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
    CreateMovieRoles,
    CreateMovieWriters,
    CreateMovieCrew,
)


def application_services_provider_factory() -> Provider:
    provider = Provider(Scope.REQUEST)

    provider.provide(AccessConcern, scope=Scope.APP)
    provider.provide(EnsurePersonsExist)
    provider.provide(CreateAndSaveRoles)
    provider.provide(DeleteRoles)
    provider.provide(CreateAndSaveWriters)
    provider.provide(DeleteWriters)
    provider.provide(CreateAndSaveCrew)
    provider.provide(DeleteCrew)
    provider.provide(CreateMovieRoles, scope=Scope.APP)
    provider.provide(CreateMovieWriters, scope=Scope.APP)
    provider.provide(CreateMovieCrew, scope=Scope.APP)

    return provider
