from redis.asyncio import Redis

from .config import RedisConfig


def redis_factory(
    redis_config: RedisConfig,
) -> Redis:
    return Redis.from_url(
        url=redis_config.url,
        decode_responses=True,
    )
