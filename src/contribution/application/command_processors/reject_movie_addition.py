import logging
from datetime import datetime, timezone

from uuid_extensions import uuid7

from contribution.domain.value_objects import AchievementId
from contribution.domain.services import RejectContribution
from contribution.application.common.command_processors import (
    CommandProcessor,
    TransactionProcessor,
)
from contribution.application.common.exceptions import (
    UserDoesNotExistError,
    ContributionDoesNotExistError,
)
from contribution.application.common.gateways import (
    AddMovieContributionGateway,
    UserGateway,
    AchievementGateway,
)
from contribution.application.common.unit_of_work import UnitOfWork
from contribution.application.common.callbacks import OnAchievementEarned
from contribution.application.commands import RejectMovieAdditionCommand


logger = logging.getLogger(__name__)


def reject_movie_addition_factory(
    reject_contribution: RejectContribution,
    add_movie_contribution_gateway: AddMovieContributionGateway,
    user_gateway: UserGateway,
    achievement_gateway: AchievementGateway,
    unit_of_work: UnitOfWork,
    on_achievement_earned: OnAchievementEarned,
) -> CommandProcessor[RejectMovieAdditionCommand, None]:
    accept_movie_addition_processor = RejectMovieAdditionProcessor(
        reject_contribution=reject_contribution,
        add_movie_contribution_gateway=add_movie_contribution_gateway,
        user_gateway=user_gateway,
        achievement_gateway=achievement_gateway,
        on_achievement_earned=on_achievement_earned,
    )
    tx_processor = TransactionProcessor(
        processor=accept_movie_addition_processor,
        unit_of_work=unit_of_work,
    )
    log_processor = LoggingProcessor(
        processor=tx_processor,
    )

    return log_processor


class RejectMovieAdditionProcessor:
    def __init__(
        self,
        *,
        reject_contribution: RejectContribution,
        add_movie_contribution_gateway: AddMovieContributionGateway,
        user_gateway: UserGateway,
        achievement_gateway: AchievementGateway,
        on_achievement_earned: OnAchievementEarned,
    ):
        self._reject_contribution = reject_contribution
        self._add_movie_contribution_gateway = add_movie_contribution_gateway
        self._user_gateway = user_gateway
        self._achievement_gateway = achievement_gateway
        self._on_achievement_earned = on_achievement_earned

    async def process(
        self,
        command: RejectMovieAdditionCommand,
    ) -> None:
        current_timestamp = datetime.now(timezone.utc)

        contribution = await self._add_movie_contribution_gateway.with_id(
            id=command.contribution_id,
        )
        if not contribution:
            raise ContributionDoesNotExistError()

        author = await self._user_gateway.acquire_with_id(
            id=contribution.author_id,
        )
        if not author:
            raise UserDoesNotExistError(contribution.author_id)

        achievement = self._reject_contribution(
            achievement_id=AchievementId(uuid7()),
            contribution=contribution,
            author=author,
            current_timestamp=current_timestamp,
        )
        if achievement:
            await self._achievement_gateway.save(achievement)

            await self._on_achievement_earned(
                id=achievement.id,
                user_id=achievement.user_id,
                achieved=achievement.achieved,
                achieved_at=current_timestamp,
            )

        await self._user_gateway.update(author)
        await self._add_movie_contribution_gateway.update(contribution)


class LoggingProcessor:
    def __init__(self, processor: TransactionProcessor):
        self._processor = processor

    async def process(
        self,
        command: RejectMovieAdditionCommand,
    ) -> None:
        logger.debug(
            msg="Processing Reject Movie Addition command",
            extra={"command": command},
        )

        try:
            result = await self._processor.process(command)
        except ContributionDoesNotExistError as e:
            logger.error(
                msg="Contribution doesn't exist",
                extra={"contribution_id": command.contribution_id},
            )
            raise e
        except UserDoesNotExistError as e:
            logger.error(
                msg=(
                    "Contribution has author id, "
                    "using which user gateway returns None"
                ),
                extra={"user_id": e.id},
            )
            raise e

        logger.debug(
            msg="Reject Movie Addition command was processed",
        )

        return result
