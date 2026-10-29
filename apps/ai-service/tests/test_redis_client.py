from app.core.config import settings
from app.redis_pubsub import client


def test_redis_client_uses_configured_url(monkeypatch):
    calls = {}

    class RedisStub:
        @classmethod
        def from_url(cls, url, **kwargs):
            calls["url"] = url
            calls["kwargs"] = kwargs
            return "url-client"

    monkeypatch.setattr(client.redis, "Redis", RedisStub)
    monkeypatch.setattr(settings, "redis_url", "rediss://cache.example:6379/0")

    assert client.create_redis_client() == "url-client"
    assert calls == {
        "url": "rediss://cache.example:6379/0",
        "kwargs": {"decode_responses": True},
    }


def test_redis_client_uses_host_settings_without_url(monkeypatch):
    calls = {}

    class RedisStub:
        def __init__(self, **kwargs):
            calls.update(kwargs)

    monkeypatch.setattr(client.redis, "Redis", RedisStub)
    monkeypatch.setattr(settings, "redis_url", None)
    monkeypatch.setattr(settings, "redis_host", "redis")
    monkeypatch.setattr(settings, "redis_port", 6380)
    monkeypatch.setattr(settings, "redis_password", "test-password")

    client.create_redis_client()

    assert calls == {
        "host": "redis",
        "port": 6380,
        "password": "test-password",
        "decode_responses": True,
    }
