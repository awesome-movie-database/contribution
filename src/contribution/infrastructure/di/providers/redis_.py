from dishka import Provider, Scope

from contribution.infrastructure.cache import redis_factory


def redis_provider_factory() -> Provider:
    provider = Provider(Scope.APP)

    provider.provide(redis_factory)

    return provider
