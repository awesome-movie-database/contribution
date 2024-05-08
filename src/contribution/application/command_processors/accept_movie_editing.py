import logging
from typing import Optional

from uuid_extensions import uuid7

from contribution.domain.value_objects import AchievementId
from contribution.domain.services import (
    AcceptContribution,
    UpdateMovie,
)
from contribution.application.common.command_processors import (
    CommandProcessor,
    TransactionProcessor,
    AchievementEearnedCallbackProcessor,
)
from contribution.application.common.exceptions import (
    MovieDoesNotExistError,
    UserDoesNotExistError,
    ContributionDoesNotExistError,
    AchievementDoesNotExistError,
)
from contribution.application.common.gateways import (
    EditMovieContributionGateway,
    MovieGateway,
    UserGateway,
    AchievementGateway,
)
from contribution.application.common.unit_of_work import UnitOfWork
from contribution.application.common.callbacks import OnAchievementEarned
from contribution.application.commands import AcceptMovieEditingCommand


logger = logging.getLogger(__name__)


def accept_movie_editing_factory(
    accept_contribution: AcceptContribution,
    update_movie: UpdateMovie,
    edit_movie_contribution_gateway: EditMovieContributionGateway,
    user_gateway: UserGateway,
    movie_gateway: MovieGateway,
    achievement_gateway: AchievementGateway,
    unit_of_work: UnitOfWork,
    on_achievement_earned: OnAchievementEarned,
) -> CommandProcessor[AcceptMovieEditingCommand, Optional[AchievementId]]:
    accept_movie_editing_processor = AcceptMovieEditingProcessor(
        accept_contribution=accept_contribution,
        update_movie=update_movie,
        edit_movie_contribution_gateway=edit_movie_contribution_gateway,
        user_gateway=user_gateway,
        movie_gateway=movie_gateway,
        achievement_gateway=achievement_gateway,
    )
    callback_processor = AchievementEearnedCallbackProcessor(
        processor=accept_movie_editing_processor,
        achievement_gateway=achievement_gateway,
        on_achievement_earned=on_achievement_earned,
    )
    tx_processor = TransactionProcessor(
        processor=callback_processor,
        unit_of_work=unit_of_work,
    )
    log_processor = LoggingProcessor(
        processor=tx_processor,
    )

    return log_processor


class AcceptMovieEditingProcessor:
    def __init__(
        self,
        *,
        accept_contribution: AcceptContribution,
        update_movie: UpdateMovie,
        edit_movie_contribution_gateway: EditMovieContributionGateway,
        user_gateway: UserGateway,
        movie_gateway: MovieGateway,
        achievement_gateway: AchievementGateway,
    ):
        self._accept_contribution = accept_contribution
        self._update_movie = update_movie
        self._edit_movie_contribution_gateway = edit_movie_contribution_gateway
        self._user_gateway = user_gateway
        self._movie_gateway = movie_gateway
        self._achievement_gateway = achievement_gateway

    async def process(
        self,
        command: AcceptMovieEditingCommand,
    ) -> Optional[AchievementId]:
        contribution = await self._edit_movie_contribution_gateway.with_id(
            id=command.contribution_id,
        )
        if not contribution:
            raise ContributionDoesNotExistError()

        author = await self._user_gateway.acquire_with_id(
            id=contribution.author_id,
        )
        if not author:
            raise UserDoesNotExistError(contribution.author_id)

        movie = await self._movie_gateway.acquire_with_id(
            id=contribution.movie_id,
        )
        if not movie:
            raise MovieDoesNotExistError()

        achievement = self._accept_contribution(
            achievement_id=AchievementId(uuid7()),
            contribution=contribution,
            author=author,
            current_timestamp=command.accepted_at,
        )
        if achievement:
            await self._achievement_gateway.save(achievement)

        await self._user_gateway.update(author)
        await self._edit_movie_contribution_gateway.update(contribution)

        self._update_movie(
            movie,
            eng_title=contribution.eng_title,
            original_title=contribution.original_title,
            release_date=contribution.release_date,
            countries=contribution.countries,
            genres=contribution.genres,
            mpaa=contribution.mpaa,
            duration=contribution.duration,
            budget=contribution.budget,
            revenue=contribution.revenue,
        )
        await self._movie_gateway.update(movie)

        return achievement.id if achievement else None


class LoggingProcessor:
    def __init__(self, processor: TransactionProcessor):
        self._processor = processor

    async def process(
        self,
        command: AcceptMovieEditingCommand,
    ) -> Optional[AchievementId]:
        command_processing_id = uuid7()

        logger.debug(
            "'Accept Movie Editing' command processing started",
            extra={
                "processing_id": command_processing_id,
                "command": command,
            },
        )

        try:
            result = await self._processor.process(command)
        except ContributionDoesNotExistError as e:
            logger.error(
                "Unexpected error occurred: Contribution doesn't exist",
                extra={"processing_id": command_processing_id},
            )
            raise e
        except UserDoesNotExistError as e:
            logger.error(
                "Unexpected error occurred: Contribution has author id, "
                "using which user gateway returns None",
                extra={"processing_id": command_processing_id},
            )
            raise e
        except MovieDoesNotExistError as e:
            logger.error(
                "Unexpected error occurred: Contribution has movie id,"
                "using which movie gateway returns None",
                extra={"processing_id": command_processing_id},
            )
            raise e
        except AchievementDoesNotExistError as e:
            logger.error(
                "Unexpected error occurred: Achievement was created, "
                "but achievement gateway returns None",
                extra={"processing_id": command_processing_id},
            )
        except Exception as e:
            logger.exception(
                "Unexpected error occurred",
                exc_info=e,
                extra={
                    "processing_id": command_processing_id,
                    "error": e,
                },
            )
            raise e

        logger.debug(
            "'Accept Movie Editing' command processing completed",
            extra={
                "processing_id": command_processing_id,
                "achievement_id": result,
            },
        )

        return result
