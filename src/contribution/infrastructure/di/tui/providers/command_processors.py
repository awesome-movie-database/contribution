from dishka import Provider, Scope

from contribution.application import (
    create_user_factory,
    update_user_factory,
    update_user_factory,
    create_movie_factory,
    update_movie_factory,
    create_person_factory,
    update_person_factory,
)


def tui_command_processors_provider_factory() -> Provider:
    provider = Provider(Scope.REQUEST)

    provider.provide(create_user_factory)
    provider.provide(update_user_factory)
    provider.provide(create_movie_factory)
    provider.provide(update_movie_factory)
    provider.provide(create_person_factory)
    provider.provide(update_person_factory)

    return provider
