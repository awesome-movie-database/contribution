from dishka import Provider, Scope

from contribution.application import (
    create_user_factory,
    update_user_factory,
    update_user_factory,
    create_movie_factory,
    update_movie_factory,
    create_person_factory,
    update_person_factory,
    add_movie_factory,
    edit_movie_factory,
    add_person_factory,
    edit_person_factory,
    accept_movie_adding_factory,
    accept_movie_editing_factory,
    accept_person_adding_factory,
    accept_person_editing_factory,
    reject_movie_adding_factory,
    reject_movie_editing_factory,
    reject_person_adding_factory,
    reject_person_editing_factory,
)


def cli_command_processors_provider_factory() -> Provider:
    provider = Provider(Scope.REQUEST)

    provider.provide(create_user_factory)
    provider.provide(update_user_factory)
    provider.provide(create_movie_factory)
    provider.provide(update_movie_factory)
    provider.provide(create_person_factory)
    provider.provide(update_person_factory)

    return provider


def web_api_command_processors_provider_factory() -> Provider:
    provider = Provider(Scope.REQUEST)

    provider.provide(add_movie_factory)
    provider.provide(edit_movie_factory)
    provider.provide(add_person_factory)
    provider.provide(edit_person_factory)

    return provider


def event_consumer_command_processors_provider_factory() -> Provider:
    provider = Provider(Scope.REQUEST)

    provider.provide(create_user_factory)
    provider.provide(update_user_factory)
    provider.provide(create_movie_factory)
    provider.provide(update_movie_factory)
    provider.provide(create_person_factory)
    provider.provide(update_person_factory)
    provider.provide(accept_movie_adding_factory)
    provider.provide(accept_movie_editing_factory)
    provider.provide(accept_person_adding_factory)
    provider.provide(accept_person_editing_factory)
    provider.provide(reject_movie_adding_factory)
    provider.provide(reject_movie_editing_factory)
    provider.provide(reject_person_adding_factory)
    provider.provide(reject_person_editing_factory)

    return provider


def tui_command_processors_provider_factory() -> Provider:
    provider = Provider(Scope.REQUEST)

    provider.provide(create_user_factory)
    provider.provide(update_user_factory)
    provider.provide(create_movie_factory)
    provider.provide(update_movie_factory)
    provider.provide(create_person_factory)
    provider.provide(update_person_factory)

    return provider
