from dishka import Provider, Scope

from contribution.domain import (
    AddMovieContributionId,
    EditMovieContributionId,
    AddPersonContributionId,
    EditPersonContributionId,
)
from contribution.application import (
    CommandProcessor,
    create_movie_factory,
    add_movie_factory,
    edit_movie_factory,
    add_person_factory,
    edit_person_factory,
    CreateMovieCommand,
    AddMovieCommand,
    EditMovieCommand,
    AddPersonCommand,
    EditPersonCommand,
)


def cli_command_processors_provider_factory() -> Provider:
    provider = Provider(Scope.REQUEST)

    provider.provide(
        create_movie_factory,
        provides=CommandProcessor[CreateMovieCommand, None],
    )

    return provider


def web_api_command_processors_provider_factory() -> Provider:
    provider = Provider(Scope.REQUEST)

    provider.provide(
        add_movie_factory,
        provides=CommandProcessor[AddMovieCommand, AddMovieContributionId],
    )
    provider.provide(
        edit_movie_factory,
        provides=CommandProcessor[EditMovieCommand, EditMovieContributionId],
    )
    provider.provide(
        add_person_factory,
        provides=CommandProcessor[AddPersonCommand, AddPersonContributionId],
    )
    provider.provide(
        edit_person_factory,
        provides=CommandProcessor[EditPersonCommand, EditPersonContributionId],
    )

    return provider
