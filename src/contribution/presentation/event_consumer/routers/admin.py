from faststream.rabbit import RabbitRouter
from dishka.integrations.faststream import FromDishka, inject

from contribution.domain import AchievementId
from contribution.application import (
    CommandProcessor,
    CreateUserCommand,
    UpdateUserCommand,
    CreateMovieCommand,
    UpdateMovieCommand,
    CreatePersonCommand,
    UpdatePersonCommand,
    AcceptMovieAddingCommand,
    AcceptMovieEditingCommand,
    AcceptPersonAddingCommand,
    AcceptPersonEditingCommand,
    RejectMovieAddingCommand,
    RejectMovieEditingCommand,
    RejectPersonAddingCommand,
    RejectPersonEditingCommand,
)


CreateUserProcessor = CommandProcessor[
    CreateUserCommand,
    None,
]
UpdateUserProcessor = CommandProcessor[
    UpdateUserCommand,
    None,
]
CreateMovieProcessor = CommandProcessor[
    CreateMovieCommand,
    None,
]
UpdateMovieProcessor = CommandProcessor[
    UpdateMovieCommand,
    None,
]
CreatePersonProcessor = CommandProcessor[
    CreatePersonCommand,
    None,
]
UpdatePersonProcessor = CommandProcessor[
    UpdatePersonCommand,
    None,
]
AcceptMovieAddingProcessor = CommandProcessor[
    AcceptMovieAddingCommand,
    AchievementId,
]
AcceptMovieEditingProcessor = CommandProcessor[
    AcceptMovieEditingCommand,
    AchievementId,
]
AcceptPersonAddingProcessor = CommandProcessor[
    AcceptPersonAddingCommand,
    AchievementId,
]
AcceptPersonEditingProcessor = CommandProcessor[
    AcceptPersonEditingCommand,
    AchievementId,
]
RejectMovieAddingProcessor = CommandProcessor[
    RejectMovieAddingCommand,
    AchievementId,
]
RejectMovieEditingProcessor = CommandProcessor[
    RejectMovieEditingCommand,
    AchievementId,
]
RejectPersonAddingProcessor = CommandProcessor[
    RejectPersonAddingCommand,
    AchievementId,
]
RejectPersonEditingProcessor = CommandProcessor[
    RejectPersonEditingCommand,
    AchievementId,
]


router = RabbitRouter()


@router.subscriber("user_created")
@inject
async def create_user(
    command: CreateUserCommand,
    command_processor: FromDishka[CreateUserProcessor],
) -> None:
    await command_processor.process(command)


@router.subscriber("user_updated")
@inject
async def update_user(
    command: UpdateUserCommand,
    command_processor: FromDishka[UpdateUserProcessor],
) -> None:
    await command_processor.process(command)


@router.subscriber("movie_created")
@inject
async def create_movie(
    command: CreateMovieCommand,
    command_processor: FromDishka[CreateMovieProcessor],
) -> None:
    await command_processor.process(command)


@router.subscriber("movie_updated")
@inject
async def update_movie(
    command: UpdateMovieCommand,
    command_processor: FromDishka[UpdateMovieProcessor],
) -> None:
    await command_processor.process(command)


@router.subscriber("person_created")
@inject
async def create_person(
    command: CreatePersonCommand,
    command_processor: FromDishka[CreatePersonProcessor],
) -> None:
    await command_processor.process(command)


@router.subscriber("person_updated")
@inject
async def update_person(
    command: UpdatePersonCommand,
    command_processor: FromDishka[UpdatePersonProcessor],
) -> None:
    await command_processor.process(command)


@router.subscriber("add_movie_contribution_accepted")
@inject
async def accept_movie_adding_contribution(
    command: AcceptMovieAddingCommand,
    command_processor: FromDishka[AcceptMovieAddingProcessor],
) -> None:
    await command_processor.process(command)


@router.subscriber("edit_movie_contribution_accepted")
@inject
async def accept_movie_editing_contribution(
    command: AcceptMovieEditingCommand,
    command_processor: FromDishka[AcceptMovieEditingProcessor],
) -> None:
    await command_processor.process(command)


@router.subscriber("add_person_contribution_accepted")
@inject
async def accept_person_adding_contribution(
    command: AcceptPersonAddingCommand,
    command_processor: FromDishka[AcceptPersonAddingProcessor],
) -> None:
    await command_processor.process(command)


@router.subscriber("edit_person_contribution_accepted")
@inject
async def accept_person_editing_contribution(
    command: AcceptPersonAddingCommand,
    command_processor: FromDishka[AcceptPersonEditingProcessor],
) -> None:
    await command_processor.process(command)


@router.subscriber("add_movie_contribution_rejected")
@inject
async def reject_movie_adding_contribution(
    command: RejectMovieAddingCommand,
    command_processor: FromDishka[RejectMovieAddingProcessor],
) -> None:
    await command_processor.process(command)


@router.subscriber("edit_movie_contribution_rejected")
@inject
async def reject_movie_editing_contribution(
    command: RejectMovieEditingCommand,
    command_processor: FromDishka[RejectMovieEditingProcessor],
) -> None:
    await command_processor.process(command)


@router.subscriber("add_person_contribution_rejected")
@inject
async def reject_person_adding_contribution(
    command: RejectPersonAddingCommand,
    command_processor: FromDishka[RejectPersonAddingProcessor],
) -> None:
    await command_processor.process(command)


@router.subscriber("edit_person_contribution_rejected")
@inject
async def reject_person_editing_contribution(
    command: RejectPersonAddingCommand,
    command_processor: FromDishka[RejectPersonEditingProcessor],
) -> None:
    await command_processor.process(command)
