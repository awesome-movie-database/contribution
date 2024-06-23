from dishka import Provider, Scope

from contribution.infrastructure.database import (
    user_collection_factory,
    movie_collection_factory,
    person_collection_factory,
    role_collection_factory,
    writer_collection_factory,
    crew_member_collection_factory,
    add_movie_contribution_collection_factory,
    edit_movie_contribution_collection_factory,
    add_person_contribution_collection_factory,
    edit_person_contribution_collection_factory,
    achievement_collection_factory,
    permissions_collection_factory,
)


def collections_provider_factory() -> Provider:
    provider = Provider(Scope.REQUEST)

    provider.provide(user_collection_factory)
    provider.provide(movie_collection_factory)
    provider.provide(person_collection_factory)
    provider.provide(role_collection_factory)
    provider.provide(writer_collection_factory)
    provider.provide(crew_member_collection_factory)
    provider.provide(add_movie_contribution_collection_factory)
    provider.provide(edit_movie_contribution_collection_factory)
    provider.provide(add_person_contribution_collection_factory)
    provider.provide(edit_person_contribution_collection_factory)
    provider.provide(achievement_collection_factory)
    provider.provide(permissions_collection_factory)

    return provider
