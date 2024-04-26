import dataclasses
from typing import Generator

import pytest
from docker.models.containers import Container

from .base import AbstractService


@dataclasses.dataclass(frozen=True)
class Redis:
    connection_string: str


class RedisService(AbstractService[Redis]):
    service_name = "redis"
    service_port = 6379
    data_path = "/data"
    proto = "redis"

    def _is_ready(self, container: Container) -> bool:
        result = container.exec_run("redis-cli ping | grep PONG")
        return result.exit_code == 0

    def _get_success_instance(self, port: int) -> Redis:
        return Redis(connection_string=f"{self.proto}://{self._host}:{port}")


@pytest.fixture(scope="session")
def redis() -> Generator[Redis, None, None]:
    with RedisService("redis:alpine").run() as r:
        yield r


@pytest.fixture(scope="session")
def redis_7() -> Generator[Redis, None, None]:
    with RedisService("redis:7-alpine").run() as pg:
        yield pg
