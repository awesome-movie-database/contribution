from dishka import Provider, Scope

from contribution.application import (
    AccessConcern,
    EnsurePersonsExist,
    ValidateRoles,
    CreateAndSaveRoles,
    DeleteRoles,
    CreateAndSaveWriters,
    DeleteWriters,
    CreateAndSaveCrew,
    DeleteCrew,
)


def application_services_provider_factory() -> Provider:
    provider = Provider(Scope.REQUEST)

    provider.provide(AccessConcern, scope=Scope.APP)
    provider.provide(EnsurePersonsExist)
    provider.provide(ValidateRoles, scope=Scope.APP)
    provider.provide(CreateAndSaveRoles)
    provider.provide(DeleteRoles)
    provider.provide(CreateAndSaveWriters)
    provider.provide(DeleteWriters)
    provider.provide(CreateAndSaveCrew)
    provider.provide(DeleteCrew)

    return provider
