from dishka import Provider, Scope

from contribution.infrastructure.cache import PermissionsCache


def cache_provider_factory() -> Provider:
    provider = Provider(Scope.REQUEST)

    provider.provide(PermissionsCache)

    return provider
