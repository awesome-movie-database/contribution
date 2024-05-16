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

    provider.provide(MovieMap, provides=MovieMap)
    provider.provide(UserMap, provides=UserMap)
    provider.provide(PersonMap, provides=PersonMap)
    provider.provide(RoleMap, provides=RoleMap)
    provider.provide(WriterMap, provides=WriterMap)
    provider.provide(CrewMemberMap, provides=CrewMemberMap)
    provider.provide(AchievementMap, provides=AchievementMap)
    provider.provide(AddMovieContributionMap, provides=AddMovieContributionMap)
    provider.provide(
        EditMovieContributionMap,
        provides=EditMovieContributionMap,
    )
    provider.provide(
        AddPersonContributionMap,
        provides=AddPersonContributionMap,
    )
    provider.provide(
        EditPersonContributionMap,
        provides=EditPersonContributionMap,
    )

    return provider
