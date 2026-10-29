import redis

from app.core.config import settings


def create_redis_client(decode_responses: bool = True) -> redis.Redis:
    if settings.redis_url:
        return redis.Redis.from_url(
            settings.redis_url,
            decode_responses=decode_responses,
        )

    return redis.Redis(
        host=settings.redis_host,
        port=settings.redis_port,
        password=settings.redis_password,
        decode_responses=decode_responses,
    )
