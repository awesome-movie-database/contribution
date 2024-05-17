from dishka import Provider, Scope

from contribution.application import (
    AccessConcern,
    EnsurePersonsExist,
    CreateAndSaveRoles,
    DeleteRoles,
    CreateAndSaveWriters,
    DeleteWriters,
    CreateAndSaveCrew,
    DeleteCrew,
    CreatePhotoFromObj,
)


def application_services_provider_factory() -> Provider:
    provider = Provider(scope=Scope.REQUEST)

    provider.provide(
        AccessConcern,
        scope=Scope.APP,
        provides=AccessConcern,
    )
    provider.provide(EnsurePersonsExist, provides=EnsurePersonsExist)
    provider.provide(CreateAndSaveRoles, provides=CreateAndSaveRoles)
    provider.provide(DeleteRoles, provides=DeleteRoles)
    provider.provide(CreateAndSaveWriters, provides=CreateAndSaveWriters)
    provider.provide(DeleteWriters, provides=DeleteWriters)
    provider.provide(CreateAndSaveCrew, provides=CreateAndSaveCrew)
    provider.provide(DeleteCrew, provides=DeleteCrew)
    provider.provide(CreatePhotoFromObj, provides=CreatePhotoFromObj)

    return provider
