import logging
from typing import Optional

from uuid_extensions import uuid7

from contribution.domain import (
    AchievementId,
    RejectContribution,
)
from contribution.application.common import (
    OperationId,
    CommandProcessor,
    TransactionProcessor,
    AchievementEearnedCallbackProcessor,
    UserDoesNotExistError,
    ContributionDoesNotExistError,
    AchievementDoesNotExistError,
    AddPersonContributionGateway,
    UserGateway,
    AchievementGateway,
    PhotoGateway,
    UnitOfWork,
    OnEventOccurred,
    AchievementEarnedEvent,
)
from contribution.application.commands import RejectPersonAddingCommand


logger = logging.getLogger(__name__)


def reject_person_adding_factory(
    operation_id: OperationId,
    reject_contribution: RejectContribution,
    add_person_contribution_gateway: AddPersonContributionGateway,
    user_gateway: UserGateway,
    achievement_gateway: AchievementGateway,
    unit_of_work: UnitOfWork,
    photo_gateway: PhotoGateway,
    on_achievement_earned: OnEventOccurred[AchievementEarnedEvent],
) -> CommandProcessor[RejectPersonAddingCommand, Optional[AchievementId]]:
    reject_person_addition_processor = RejectPersonAddingProcessor(
        reject_contribution=reject_contribution,
        add_person_contribution_gateway=add_person_contribution_gateway,
        user_gateway=user_gateway,
        achievement_gateway=achievement_gateway,
        photo_gateway=photo_gateway,
    )
    callback_processor = AchievementEearnedCallbackProcessor(
        processor=reject_person_addition_processor,
        achievement_gateway=achievement_gateway,
        on_achievement_earned=on_achievement_earned,
    )
    tx_processor = TransactionProcessor(
        processor=callback_processor,
        unit_of_work=unit_of_work,
    )
    log_processor = RejectPersonAddingLoggingProcessor(
        processor=tx_processor,
        operation_id=operation_id,
    )

    return log_processor


class RejectPersonAddingProcessor:
    def __init__(
        self,
        *,
        reject_contribution: RejectContribution,
        add_person_contribution_gateway: AddPersonContributionGateway,
        user_gateway: UserGateway,
        achievement_gateway: AchievementGateway,
        photo_gateway: PhotoGateway,
    ):
        self._reject_contribution = reject_contribution
        self._add_person_contribution_gateway = add_person_contribution_gateway
        self._user_gateway = user_gateway
        self._achievement_gateway = achievement_gateway
        self._photo_gateway = photo_gateway

    async def process(
        self,
        command: RejectPersonAddingCommand,
    ) -> Optional[AchievementId]:
        contribution = (
            await self._add_person_contribution_gateway.acquire_by_id(
                id=command.contribution_id,
            )
        )
        if not contribution:
            raise ContributionDoesNotExistError()

        author = await self._user_gateway.acquire_by_id(
            id=contribution.author_id,
        )
        if not author:
            raise UserDoesNotExistError()

        achievement = self._reject_contribution(
            achievement_id=AchievementId(uuid7()),
            contribution=contribution,
            author=author,
            current_timestamp=command.rejected_at,
        )
        if achievement:
            await self._achievement_gateway.save(achievement)

        await self._user_gateway.update(author)
        await self._add_person_contribution_gateway.update(contribution)

        await self._photo_gateway.delete_by_urls(contribution.photos)

        return achievement.id if achievement else None


class RejectPersonAddingLoggingProcessor:
    def __init__(
        self,
        *,
        processor: TransactionProcessor,
        operation_id: OperationId,
    ):
        self._processor = processor
        self._operation_id = operation_id

    async def process(
        self,
        command: RejectPersonAddingCommand,
    ) -> Optional[AchievementId]:
        self._operation_id = uuid7()

        logger.debug(
            "'Reject Person Adding' command processing started",
            extra={
                "operation_id": self._operation_id,
                "command": command,
            },
        )

        try:
            result = await self._processor.process(command)
        except ContributionDoesNotExistError as e:
            logger.error(
                "Unexpected error occurred: Contribution doesn't exist",
                extra={"operation_id": self._operation_id},
            )
            raise e
        except UserDoesNotExistError as e:
            logger.error(
                "Unexpected error occurred: Contribution has author id, "
                "using which user gateway returns None",
                extra={"operation_id": self._operation_id},
            )
            raise e
        except AchievementDoesNotExistError as e:
            logger.error(
                "Unexpected error occurred: Achievement was created, "
                "but achievement gateway returns None",
                extra={"operation_id": self._operation_id},
            )
        except Exception as e:
            logger.exception(
                "Unexpected error occurred",
                extra={
                    "operation_id": self._operation_id,
                    "error": e,
                },
            )
            raise e

        logger.debug(
            "'Reject Person Adding' command processing completed",
            extra={
                "operation_id": self._operation_id,
                "achievement_id": result,
            },
        )

        return result
