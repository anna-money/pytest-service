import pytest_service


def test_mongo(mongo: pytest_service.Mongo) -> None:
    assert mongo


def test_mongo_5(mongo_5: pytest_service.Mongo) -> None:
    assert mongo_5


def test_mongo_6(mongo_6: pytest_service.Mongo) -> None:
    assert mongo_6
