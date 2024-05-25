from dishka import Provider, Scope

from contribution.infrastructure.database import (
    MovieMap,
    UserMap,
    PersonMap,
    RoleMap,
    WriterMap,
    CrewMemberMap,
    AchievementMap,
    AddMovieContributionMap,
    EditMovieContributionMap,
    AddPersonContributionMap,
    EditPersonContributionMap,
)


def identity_maps_provider_factory() -> Provider:
    provider = Provider(scope=Scope.REQUEST)

    provider.provide(MovieMap)
    provider.provide(UserMap)
    provider.provide(PersonMap)
    provider.provide(RoleMap)
    provider.provide(WriterMap)
    provider.provide(CrewMemberMap)
    provider.provide(AchievementMap)
    provider.provide(AddMovieContributionMap)
    provider.provide(EditMovieContributionMap)
    provider.provide(AddPersonContributionMap)
    provider.provide(EditPersonContributionMap)

    return provider
