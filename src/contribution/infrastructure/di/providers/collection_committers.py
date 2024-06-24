from dishka import Provider, Scope

from contribution.infrastructure.database import (
    CommitUserCollectionChanges,
    CommitMovieCollectionChanges,
    CommitPersonCollectionChanges,
    CommitRoleCollectionChanges,
    CommitWriterCollectionChanges,
    CommitCrewMemberCollectionChanges,
    CommitAddMovieContributionCollectionChanges,
    CommitEditMovieContributionCollectionChanges,
    CommitAddPersonContributionCollectionChanges,
    CommitEditPersonContributionCollectionChanges,
    CommitAchievementCollectionChanges,
)


def collection_committers_provider_factory() -> Provider:
    provider = Provider(Scope.REQUEST)

    provider.provide(CommitUserCollectionChanges)
    provider.provide(CommitMovieCollectionChanges)
    provider.provide(CommitPersonCollectionChanges)
    provider.provide(CommitRoleCollectionChanges)
    provider.provide(CommitWriterCollectionChanges)
    provider.provide(CommitCrewMemberCollectionChanges)
    provider.provide(CommitAddMovieContributionCollectionChanges)
    provider.provide(CommitEditMovieContributionCollectionChanges)
    provider.provide(CommitAddPersonContributionCollectionChanges)
    provider.provide(CommitEditPersonContributionCollectionChanges)
    provider.provide(CommitAchievementCollectionChanges)

    return provider
