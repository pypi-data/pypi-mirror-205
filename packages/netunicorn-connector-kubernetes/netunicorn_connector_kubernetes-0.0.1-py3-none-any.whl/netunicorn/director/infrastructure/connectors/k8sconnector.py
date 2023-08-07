from __future__ import annotations

import asyncio
import logging
from logging import Logger
from multiprocessing.pool import ApplyResult
from typing import Any, NoReturn, Optional, Tuple

import yaml
from kubernetes import client, config
from netunicorn.base.architecture import Architecture
from netunicorn.base.deployment import Deployment
from netunicorn.base.environment_definitions import DockerImage
from netunicorn.base.nodes import CountableNodePool, Node, Nodes
from netunicorn.director.base.connectors.protocol import NetunicornConnectorProtocol
from netunicorn.director.base.connectors.types import StopExecutorRequest
from returns.result import Failure, Result, Success


class KubernetesConnector(NetunicornConnectorProtocol):
    def __init__(
        self,
        connector_name: str,
        configuration: str | None,
        netunicorn_gateway: str,
        logger: Optional[Logger] = None,
    ):
        self.connector_name = connector_name
        self.configuration = configuration
        with open(self.configuration) as f:
            self.configuration = yaml.safe_load(f)

        self.show_node_addresses = bool(
            self.configuration.get("netunicorn.kubernetes.show_node_addresses", False)
        )
        self.show_node_labels = bool(
            self.configuration.get("netunicorn.kubernetes.show_node_labels", False)
        )
        self.namespace = self.configuration.get(
            "netunicorn.kubernetes.namespace", "netunicorn"
        )
        self.create_namespace = bool(
            self.configuration.get(
                "netunicorn.kubernetes.namespace.create_if_not_exist", False
            )
        )

        self.netunicorn_gateway = netunicorn_gateway
        self.logger = logger or logging.getLogger(__name__)

        config.load_kube_config(
            self.configuration.get("netunicorn.kubernetes.config_file", None)
        )
        self.core_api = client.CoreV1Api()
        self.apps_api = client.AppsV1Api()

        self._cleanup_task_holder: Optional[asyncio.Task] = None
        self.logger.info("Kubernetes connector initialized")

    async def _cleanup_task(self) -> NoReturn:
        self.logger.info("Starting cleanup pods task")
        while True:
            try:
                pods = self.core_api.list_namespaced_pod(self.namespace)
                current_pods_services = {
                    f"service-{pod.metadata.name}" for pod in pods.items
                }
                for pod in pods.items:
                    if pod.status.phase in {"Succeeded", "Failed", "Unknown"}:
                        self.core_api.delete_namespaced_pod(
                            pod.metadata.name, self.namespace
                        )
                        self.logger.debug(f"Deleted pod {pod.metadata.name}")
                        current_pods_services.remove(f"service-{pod.metadata.name}")

                services = self.core_api.list_namespaced_service(self.namespace)
                for service in services.items:
                    if service.metadata.name not in current_pods_services:
                        self.core_api.delete_namespaced_service(
                            service.metadata.name, self.namespace
                        )
                        self.logger.debug(f"Deleted service {service.metadata.name}")
            except Exception as e:
                self.logger.exception(e)
            await asyncio.sleep(60)

    async def initialize(self, *args: Any, **kwargs: Any) -> None:
        self._cleanup_task_holder = asyncio.create_task(self._cleanup_task())
        if self.create_namespace:
            namespaces = self.core_api.list_namespace()
            if self.namespace not in [item.metadata.name for item in namespaces.items]:
                self.core_api.create_namespace(
                    client.V1Namespace(
                        metadata=client.V1ObjectMeta(name=self.namespace)
                    )
                )
                self.logger.info(f"Created namespace {self.namespace}")

    async def health(self, *args: Any, **kwargs: Any) -> Tuple[bool, str]:
        try:
            namespaces = self.core_api.list_namespace()
            if self.namespace not in [item.metadata.name for item in namespaces.items]:
                return False, f"Namespace {self.namespace} not found"
            return True, "OK"
        except Exception as e:
            self.logger.exception(e)
            return False, str(e)

    async def shutdown(self, *args: Any, **kwargs: Any) -> None:
        if self._cleanup_task_holder:
            self._cleanup_task_holder.cancel()

    async def get_nodes(
        self,
        username: str,
        authentication_context: Optional[dict[str, str]] = None,
        *args: Any,
        **kwargs: Any,
    ) -> Nodes:
        result = self.core_api.list_node()
        pool = []

        for item in result.items:
            architecture = Architecture.UNKNOWN
            if item.status.node_info.operating_system == "linux":
                match item.status.node_info.architecture:
                    case "amd64":
                        architecture = Architecture.LINUX_AMD64
                    case "arm64":
                        architecture = Architecture.LINUX_ARM64

            node = Node(
                name=item.metadata.name,
                properties={},
                architecture=architecture,
            )
            node.properties["conditions"] = item.status.conditions
            node.properties["cpu"] = item.status.capacity.get("cpu")
            node.properties["memory"] = item.status.capacity.get("memory")
            node.properties["gpu"] = item.status.capacity.get("nvidia.com/gpu")

            if self.show_node_addresses:
                node.properties["addresses"] = item.status.addresses

            if self.show_node_labels:
                node.properties["labels"] = item.metadata.labels

            pool.append(node)

        self.logger.debug(f"Retrieved {len(pool)} nodes from Kubernetes API")
        return CountableNodePool(pool)

    async def deploy(
        self,
        username: str,
        experiment_id: str,
        deployments: list[Deployment],
        deployment_context: Optional[dict[str, str]],
        authentication_context: Optional[dict[str, str]] = None,
        *args: Any,
        **kwargs: Any,
    ) -> dict[str, Result[Optional[str], str]]:
        result: dict[str, Result[None, str]] = {}
        for deployment in deployments:
            result[deployment.executor_id] = (
                Success(None)
                .bind(
                    lambda x: Success(x)
                    if deployment.prepared
                    else Failure("Deployment is not prepared")
                )
                .bind(
                    lambda x: Success(x)
                    if isinstance(deployment.environment_definition, DockerImage)
                    else Failure("Kubernetes only supports DockerImage deployments")
                )
            )
        return result

    def _create_objects(
        self, deployment: Deployment, experiment_id: str
    ) -> Result[tuple[ApplyResult, Optional[ApplyResult]], str]:
        deployment.environment_definition.runtime_context.environment_variables[
            "NETUNICORN_GATEWAY_ENDPOINT"
        ] = self.netunicorn_gateway
        deployment.environment_definition.runtime_context.environment_variables[
            "NETUNICORN_EXPERIMENT_ID"
        ] = experiment_id
        deployment.environment_definition.runtime_context.environment_variables[
            "NETUNICORN_EXECUTOR_ID"
        ] = deployment.executor_id

        pod = client.V1Pod(
            metadata=client.V1ObjectMeta(
                name=deployment.executor_id,
                labels={
                    "netunicorn/experiment": experiment_id,
                    "netunicorn/executor": deployment.executor_id,
                },
            ),
            spec=client.V1PodSpec(
                containers=[
                    client.V1Container(
                        name=deployment.executor_id,
                        image=deployment.environment_definition.image,
                        image_pull_policy="IfNotPresent",
                        env=[
                            client.V1EnvVar(name=key, value=value)
                            for key, value in deployment.environment_definition.runtime_context.environment_variables.items()
                        ],
                        ports=[
                            client.V1ContainerPort(
                                name=f"port-{container_port}",
                                container_port=container_port,
                            )
                            for host_port, container_port in deployment.environment_definition.runtime_context.ports_mapping.items()
                        ],
                    )
                ],
                restart_policy="Never",
                node_name=deployment.node.name,
            ),
        )

        service = None
        if deployment.environment_definition.runtime_context.ports_mapping:
            ports = []
            for (
                host_port,
                container_port,
            ) in (
                deployment.environment_definition.runtime_context.ports_mapping.items()
            ):
                ports.append(
                    client.V1ServicePort(
                        name=f"nodeport-{host_port}-{container_port}-tcp",
                        port=container_port,
                        node_port=host_port,
                        protocol="TCP",
                    )
                )
                ports.append(
                    client.V1ServicePort(
                        name=f"nodeport-{host_port}-{container_port}-udp",
                        port=container_port,
                        node_port=host_port,
                        protocol="UDP",
                    )
                )

            service = client.V1Service(
                metadata=client.V1ObjectMeta(
                    name=f"service-{deployment.executor_id}",
                    labels={
                        "netunicorn/experiment": experiment_id,
                        "netunicorn/executor": deployment.executor_id,
                    },
                ),
                spec=client.V1ServiceSpec(
                    type="NodePort",
                    ports=ports,
                    selector={
                        "pod": deployment.executor_id,
                    },
                ),
            )

        try:
            pod_thread = self.core_api.create_namespaced_pod(
                namespace=self.namespace,
                body=pod,
                async_req=True,
            )
            service_thread = None
            if service:
                service_thread = self.core_api.create_namespaced_service(
                    namespace=self.namespace,
                    body=service,
                    async_req=True,
                )
            return Success((pod_thread, service_thread))
        except Exception as e:
            message = f"Failed to create pod or service {deployment.executor_id}: {e}"
            self.logger.error(message)
            return Failure(message)

    def _validate_execution(
        self,
        object_threads: tuple[ApplyResult, Optional[ApplyResult]],
    ) -> Result[str, str]:
        pod_thread, service_thread = object_threads
        message = ""

        try:
            pod = pod_thread.get()
            message += f"Successfully created pod {pod.metadata.name}, current status: {pod.status.phase}."
            if service_thread:
                service = service_thread.get()
                message += f" Successfully created service {service.metadata.name}."
            self.logger.debug(message)
            return Success(message)
        except Exception as e:
            message += f" Failed to create pod or service: {e}"
            self.logger.error(message)
            return Failure(message)

    async def execute(
        self,
        username: str,
        experiment_id: str,
        deployments: list[Deployment],
        execution_context: Optional[dict[str, str]],
        authentication_context: Optional[dict[str, str]] = None,
        *args: Any,
        **kwargs: Any,
    ) -> dict[str, Result[Optional[str], str]]:
        result = {}
        for deployment in deployments:
            if not deployment.prepared:
                result[deployment.executor_id] = Failure("Deployment is not prepared")
                continue
            if not isinstance(deployment.environment_definition, DockerImage):
                result[deployment.executor_id] = Failure(
                    "Kubernetes only supports DockerImage deployments"
                )
                continue
        deployments = [
            deployment
            for deployment in deployments
            if deployment.executor_id not in result
        ]

        # start parallel pods creation
        for deployment in deployments:
            result[deployment.executor_id] = self._create_objects(
                deployment, experiment_id
            )

        # collect results of pod creation
        for deployment in deployments:
            result[deployment.executor_id] = result[deployment.executor_id].bind(
                self._validate_execution
            )

        return result

    async def stop_executors(
        self,
        username: str,
        requests_list: list[StopExecutorRequest],
        cancellation_context: Optional[dict[str, str]],
        authentication_context: Optional[dict[str, str]] = None,
        *args: Any,
        **kwargs: Any,
    ) -> dict[str, Result[Optional[str], str]]:
        result = {}
        for request in requests_list:
            try:
                self.core_api.delete_namespaced_pod(
                    name=request["executor_id"],
                    namespace=self.namespace,
                )
                self.core_api.delete_namespaced_service(
                    name=f"service-{request['executor_id']}",
                    namespace=self.namespace,
                )
                result[request["executor_id"]] = Success(None)
            except Exception as e:
                self.logger.exception(e)
                result[request["executor_id"]] = Failure(str(e))
        return result

    async def cleanup(
        self,
        experiment_id: str,
        deployments: list[Deployment],
        *args: Any,
        **kwargs: Any,
    ) -> None:
        # cleanup infrastructure after experiment is finished
        # example for docker infrastructure
        for deployment in deployments:
            try:
                self.core_api.delete_namespaced_pod(
                    name=deployment.executor_id,
                    namespace=self.namespace,
                    async_req=True,
                )
                self.core_api.delete_namespaced_service(
                    name=f"service-{deployment.executor_id}",
                    namespace=self.namespace,
                    async_req=True,
                )
            except Exception as e:
                self.logger.exception(e)


async def test():
    from uuid import uuid4

    import cloudpickle  # you'll need it for tests

    from netunicorn import Pipeline

    connector = KubernetesConnector(
        connector_name="kubernetes-test-connector",
        configuration="configuration-example.yaml",
        netunicorn_gateway="http://localhost:8000",
    )
    await connector.initialize()
    print(await connector.health())
    nodes = await connector.get_nodes("test")
    print(nodes)

    # create dummy pipeline
    pipeline = Pipeline()
    pipeline.environment_definition.image = "ubuntu:latest"
    pipeline.environment_definition.runtime_context.ports_mapping = {30001: 80}
    deployment = Deployment(node=nodes.take(1)[0], pipeline=pipeline)
    deployment.prepared = True
    deployment.executor_id = str(uuid4())
    deployment_result = await connector.deploy(
        username="test",
        experiment_id="test",
        deployments=[deployment],
        deployment_context={},
    )
    print(deployment_result)
    execution_result = await connector.execute(
        username="test",
        experiment_id="test",
        deployments=[deployment],
        execution_context={},
    )
    print(execution_result)

    await connector.cleanup(
        experiment_id="test",
        deployments=[deployment],
    )

    await asyncio.sleep(5)


if __name__ == "__main__":
    asyncio.run(test())
