import abc
import contextlib
import socket
import time
import uuid
from typing import Any, Dict, Generator, Generic, TypeVar, Union, cast

import docker.types
import pytest
from docker.models.containers import Container

LOCALHOST = "127.0.0.1"
T = TypeVar("T")


class AbstractService(abc.ABC, Generic[T]):
    __slots__ = ("_image", "_host", "_ready_timeout", "__client")

    service_name: str
    service_port: int
    data_path: str

    @contextlib.contextmanager
    def run(self) -> Generator[T, None, None]:
        unused_port = self.find_unused_local_port()
        try:
            container = cast(
                Container,
                self._client.containers.run(
                    name=f"pytest-service-{self.service_name}-{uuid.uuid4()}",
                    image=self._image,
                    environment=self._get_container_environment(),
                    command=self._get_container_command(),
                    ports={self.service_port: unused_port},
                    detach=True,
                    tmpfs={self.data_path: ""},
                    stderr=True,
                    **self._get_container_kwargs(),
                ),
            )

            started_at = time.time()
            while time.time() - started_at < self._ready_timeout:
                container.reload()
                if container.status == "running" and self._is_ready(container):
                    break

                time.sleep(0.5)
            else:
                assert container.id
                raw_logs = cast(bytes, self._client.api.logs(container.id))
                pytest.fail(
                    f"Failed to start {self.service_name} using {self._image} in {self._ready_timeout}"
                    f" seconds: {raw_logs.decode()}"
                )

            yield self._get_success_instance(unused_port)

            container.reload()
            if container.status == "running":
                container.kill()
            container.remove(v=True, force=True)
        finally:
            self._client.close()

    def _get_container_environment(self) -> Union[Dict[str, str], None]:
        return None

    def _get_container_command(self) -> Union[str, None]:
        return None

    def _get_container_kwargs(self) -> Dict[str, Any]:
        return {}

    @abc.abstractmethod
    def _is_ready(self, container: Container) -> bool: ...

    @abc.abstractmethod
    def _get_success_instance(self, port: int) -> T: ...

    def find_unused_local_port(self) -> int:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self._host, 0))
            return s.getsockname()[1]  # type: ignore

    @property
    def _client(self) -> docker.DockerClient:
        if self.__client is None:
            self.__client = docker.from_env()
        return self.__client

    def __init__(self, image: str, *, host: str = LOCALHOST, ready_timeout: float = 30.0) -> None:
        self._image = image
        self._host = host
        self._ready_timeout = ready_timeout
        self.__client = None
