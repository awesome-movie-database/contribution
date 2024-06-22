from dishka import Provider, Scope
from fastapi import Request

from contribution.application import IdentityProvider
from contribution.infrastructure.identity import RawIdentityProvider


def identity_provider_provider_factory() -> Provider:
    provider = Provider(Scope.REQUEST)

    provider.from_context(Request)
    provider.provide(RawIdentityProvider, provides=IdentityProvider)

    return provider
