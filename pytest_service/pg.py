import dataclasses
from typing import Dict, Generator, Union

import pytest
from docker.models.containers import Container

from .base import AbstractService
from .utils import is_pg_ready


@dataclasses.dataclass(frozen=True)
class PG:
    host: str
    port: int
    user: str
    password: str
    database: str


class PGService(AbstractService[PG]):
    __slots__ = ()

    DEFAULT_PG_USER = "postgres"
    DEFAULT_PG_PASSWORD = "my-secret-password"
    DEFAULT_PG_DATABASE = "postgres"

    service_name = "postgres"
    service_port = 5432
    data_path = "/var/lib/postgresql/data"

    def _get_container_environment(self) -> Union[Dict[str, str], None]:
        return {
            "POSTGRES_HOST_AUTH_METHOD": "trust",
            "PGDATA": self.data_path,
        }

    def _get_container_command(self) -> Union[str, None]:
        return "-c fsync=off -c full_page_writes=off -c synchronous_commit=off -c bgwriter_lru_maxpages=0 -c jit=off"

    def _is_ready(self, container: Container) -> bool:
        bindings = (container.attrs or {}).get("HostConfig", {}).get("PortBindings", {})
        assert bindings
        port = bindings[f"{self.service_port}/tcp"][0]["HostPort"]
        return is_pg_ready(
            host=self._host,
            port=port,
            database=self.DEFAULT_PG_DATABASE,
            user=self.DEFAULT_PG_USER,
            password=self.DEFAULT_PG_PASSWORD,
        )

    def _get_success_instance(self, port: int) -> PG:
        return PG(
            host=self._host,
            port=port,
            user=self.DEFAULT_PG_USER,
            password=self.DEFAULT_PG_PASSWORD,
            database=self.DEFAULT_PG_DATABASE,
        )


@pytest.fixture(scope="session")
def pg() -> Generator[PG, None, None]:
    with PGService("postgres:latest").run() as pg:
        yield pg


@pytest.fixture(scope="session")
def pg_11() -> Generator[PG, None, None]:
    with PGService("postgres:11").run() as pg:
        yield pg


@pytest.fixture(scope="session")
def pg_12() -> Generator[PG, None, None]:
    with PGService("postgres:12").run() as pg:
        yield pg


@pytest.fixture(scope="session")
def pg_13() -> Generator[PG, None, None]:
    with PGService("postgres:13").run() as pg:
        yield pg


@pytest.fixture(scope="session")
def pg_14() -> Generator[PG, None, None]:
    with PGService("postgres:14").run() as pg:
        yield pg


@pytest.fixture(scope="session")
def pg_15() -> Generator[PG, None, None]:
    with PGService("postgres:15").run() as pg:
        yield pg


@pytest.fixture(scope="session")
def pg_16() -> Generator[PG, None, None]:
    with PGService("postgres:16").run() as pg:
        yield pg
