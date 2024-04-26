import pytest_service


def test_redis(redis: pytest_service.Redis) -> None:
    assert redis


def test_redis_7(redis_7: pytest_service.Redis) -> None:
    assert redis_7
