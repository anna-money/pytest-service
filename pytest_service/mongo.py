import dataclasses
from typing import Generator

import pytest
from docker.models.containers import Container

from .base import AbstractService


@dataclasses.dataclass(frozen=True)
class Mongo:
    connection_string: str


class MongoDBService(AbstractService[Mongo]):
    service_name = "mongodb"
    service_port = 27017
    data_path = "/data"

    def _is_ready(self, container: Container) -> bool:
        result = container.exec_run("echo 'db.runCommand(\"ping\").ok' | mongosh mongo:27017/test --quiet")
        return result.exit_code == 0

    def _get_success_instance(self, port: int) -> Mongo:
        return Mongo(connection_string=f"{self._host}:{port}")


@pytest.fixture(scope="session")
def mongo() -> Generator[Mongo, None, None]:
    with MongoDBService("mongo:latest").run() as pg:
        yield pg


@pytest.fixture(scope="session")
def mongo_5() -> Generator[Mongo, None, None]:
    with MongoDBService("mongo:5").run() as pg:
        yield pg


@pytest.fixture(scope="session")
def mongo_6() -> Generator[Mongo, None, None]:
    with MongoDBService("mongo:6").run() as pg:
        yield pg
