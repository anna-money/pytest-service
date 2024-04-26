# pytest-service

Inspired by [pytest-pg](https://pypi.org/project/pytest-pg/) but with `MongoDB` onboard

### How to use

#### Postgres

```python
@pytest.fixture(scope="session")
def pg_14_local() -> Iterator:
    with pytest_service.PGService("postgres:14.4-alpine").run() as pg:
        yield pg


@pytest.fixture(scope="session", autouse=True)
def init_env(pg_14_local: pytest_service.PG) -> None:
    if not pg_14_local:
        return
    os.environ["POSTGRES_DBNAME"] = pg_14_local.database
    os.environ["POSTGRES_USER"] = pg_14_local.user
    os.environ["POSTGRES_PASSWORD"] = pg_14_local.password
    os.environ["POSTGRES_HOST"] = pg_14_local.host
    os.environ["POSTGRES_PORT"] = str(pg_14_local.port)

```

#### MongoDB

```python
@pytest.fixture(scope="session")
def mongo_6_local() -> Iterator:
    with pytest_service.MongoDBService("mongo:6").run() as mongo:
        yield mongo


@pytest.fixture(scope="session", autouse=True)
def init_env(mongo_6_local: pytest_service.Mongo) -> None:
    if not mongo_6_local:
        return
    os.environ["MONGODB_CONNECTION_STRING"] = mongo_6_local.connection_string

```
