from typing import AsyncGenerator

from redis.asyncio import Redis

from .config import RedisConfig


async def redis_factory(
    redis_config: RedisConfig,
) -> AsyncGenerator[Redis, None]:
    redis = Redis.from_url(
        url=redis_config.url,
        decode_responses=True,
    )
    try:
        yield redis
    finally:
        await redis.close()
