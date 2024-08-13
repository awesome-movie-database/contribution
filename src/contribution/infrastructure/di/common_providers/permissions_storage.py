from dishka import Provider, Scope, AnyOf

from contribution.application import PermissionsGateway
from contribution.infrastructure.identity import PermissionsStorage


def permissions_storage_provider_factory() -> Provider:
    provider = Provider(Scope.REQUEST)

    provider.provide(
        PermissionsStorage,
        provides=AnyOf[PermissionsGateway, PermissionsStorage],
    )

    return provider
