from dishka import Provider, Scope
from redis.asyncio import Redis

from contribution.infrastructure.cache import RedisConfig


def redis_provider_factory() -> Provider:
    provider = Provider(Scope.APP)

    provider.provide(redis_factory)

    return provider


def redis_factory(redis_config: RedisConfig) -> Redis:
    return Redis.from_url(
        url=redis_config.url,
        decode_responses=True,
    )
