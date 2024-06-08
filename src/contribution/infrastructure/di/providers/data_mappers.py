from dishka import Provider, Scope

from contribution.application import (
    UserGateway,
    MovieGateway,
    PersonGateway,
    RoleGateway,
    WriterGateway,
    CrewMemberGateway,
    AchievementGateway,
    AddMovieContributionGateway,
    EditMovieContributionGateway,
    AddPersonContributionGateway,
    EditPersonContributionGateway,
)
from contribution.infrastructure.database import (
    UserMapper,
    MovieMapper,
    PersonMapper,
    RoleMapper,
    WriterMapper,
    CrewMemberMapper,
    AddMovieContributionMapper,
    EditMovieContributionMapper,
    AddPersonContributionMapper,
    EditPersonContributionMapper,
    AchievementMapper,
)


def data_mappers_provider_factory() -> Provider:
    provider = Provider(Scope.REQUEST)

    provider.provide(UserMapper, provides=UserGateway)
    provider.provide(MovieMapper, provides=MovieGateway)
    provider.provide(PersonMapper, provides=PersonGateway)
    provider.provide(RoleMapper, provides=RoleGateway)
    provider.provide(WriterMapper, provides=WriterGateway)
    provider.provide(CrewMemberMapper, provides=CrewMemberGateway)
    provider.provide(
        AddMovieContributionMapper,
        provides=AddMovieContributionGateway,
    )
    provider.provide(
        EditMovieContributionMapper,
        provides=EditMovieContributionGateway,
    )
    provider.provide(
        AddPersonContributionMapper,
        provides=AddPersonContributionGateway,
    )
    provider.provide(
        EditPersonContributionMapper,
        provides=EditPersonContributionGateway,
    )
    provider.provide(AchievementMapper, provides=AchievementGateway)

    return provider
