from dishka import Provider, Scope

from contribution.application import (
    create_movie_factory,
    add_movie_factory,
    edit_movie_factory,
    add_person_factory,
    edit_person_factory,
)


def cli_command_processors_provider_factory() -> Provider:
    provider = Provider(Scope.REQUEST)

    provider.provide(create_movie_factory)

    return provider


def web_api_command_processors_provider_factory() -> Provider:
    provider = Provider(Scope.REQUEST)

    provider.provide(add_movie_factory)
    provider.provide(edit_movie_factory)
    provider.provide(add_person_factory)
    provider.provide(edit_person_factory)

    return provider
