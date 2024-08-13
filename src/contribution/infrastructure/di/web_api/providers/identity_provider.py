from dishka import Provider, Scope

from contribution.application import IdentityProvider
from contribution.infrastructure.identity import (
    web_api_identity_provider_factory,
)


def web_api_identity_provider_provider_factory() -> Provider:
    provider = Provider(Scope.REQUEST)

    provider.provide(
        web_api_identity_provider_factory,
        provides=IdentityProvider,
    )

    return provider
