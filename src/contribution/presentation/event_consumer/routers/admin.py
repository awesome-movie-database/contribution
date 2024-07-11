from faststream.rabbit import RabbitRouter
from dishka.integrations.faststream import FromDishka, inject

from contribution.domain import AchievementId
from contribution.application import (
    CommandProcessor,
    AcceptMovieAddingCommand,
    AcceptMovieEditingCommand,
    AcceptPersonAddingCommand,
    AcceptPersonEditingCommand,
    RejectMovieAddingCommand,
    RejectMovieEditingCommand,
    RejectPersonAddingCommand,
    RejectPersonEditingCommand,
)


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
