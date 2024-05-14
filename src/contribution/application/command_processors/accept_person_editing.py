import logging
from typing import Optional

from uuid_extensions import uuid7

from contribution.domain.value_objects import AchievementId
from contribution.domain.exceptions import (
    InvalidPersonFirstNameError,
    InvalidPersonLastNameError,
    InvalidPersonBirthOrDeathDateError,
)
from contribution.domain.services import (
    AcceptContribution,
    UpdatePerson,
)
from contribution.application.common.command_processors import (
    CommandProcessor,
    TransactionProcessor,
    AchievementEearnedCallbackProcessor,
)
from contribution.application.common.exceptions import (
    PersonDoesNotExistError,
    UserDoesNotExistError,
    ContributionDoesNotExistError,
    AchievementDoesNotExistError,
)
from contribution.application.common.gateways import (
    EditPersonContributionGateway,
    PersonGateway,
    UserGateway,
    AchievementGateway,
)
from contribution.application.common.unit_of_work import UnitOfWork
from contribution.application.common.event_callback import OnEventOccurred
from contribution.application.common.events import AchievementEarnedEvent
from contribution.application.commands import AcceptPersonEditingCommand


logger = logging.getLogger(__name__)


def accept_person_editing_factory(
    accept_contribution: AcceptContribution,
    update_person: UpdatePerson,
    edit_person_contribution_gateway: EditPersonContributionGateway,
    user_gateway: UserGateway,
    person_gateway: PersonGateway,
    achievement_gateway: AchievementGateway,
    unit_of_work: UnitOfWork,
    on_achievement_earned: OnEventOccurred[AchievementEarnedEvent],
) -> CommandProcessor[AcceptPersonEditingCommand, Optional[AchievementId]]:
    accept_person_editing_processor = AcceptPersonEditingProcessor(
        accept_contribution=accept_contribution,
        update_person=update_person,
        edit_person_contribution_gateway=edit_person_contribution_gateway,
        user_gateway=user_gateway,
        person_gateway=person_gateway,
        achievement_gateway=achievement_gateway,
    )
    callback_processor = AchievementEearnedCallbackProcessor(
        processor=accept_person_editing_processor,
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


class AcceptPersonEditingProcessor:
    def __init__(
        self,
        *,
        accept_contribution: AcceptContribution,
        update_person: UpdatePerson,
        edit_person_contribution_gateway: EditPersonContributionGateway,
        user_gateway: UserGateway,
        person_gateway: PersonGateway,
        achievement_gateway: AchievementGateway,
    ):
        self._accept_contribution = accept_contribution
        self._update_person = update_person
        self._edit_person_contribution_gateway = (
            edit_person_contribution_gateway
        )
        self._user_gateway = user_gateway
        self._person_gateway = person_gateway
        self._achievement_gateway = achievement_gateway

    async def process(
        self,
        command: AcceptPersonEditingCommand,
    ) -> Optional[AchievementId]:
        contribution = await self._edit_person_contribution_gateway.with_id(
            id=command.contribution_id,
        )
        if not contribution:
            raise ContributionDoesNotExistError()

        author = await self._user_gateway.acquire_with_id(
            id=contribution.author_id,
        )
        if not author:
            raise UserDoesNotExistError(contribution.author_id)

        person = await self._person_gateway.acquire_with_id(
            id=contribution.person_id,
        )
        if not person:
            raise PersonDoesNotExistError()

        achievement = self._accept_contribution(
            achievement_id=AchievementId(uuid7()),
            contribution=contribution,
            author=author,
            current_timestamp=command.accepted_at,
        )
        if achievement:
            await self._achievement_gateway.save(achievement)

        await self._user_gateway.update(author)
        await self._edit_person_contribution_gateway.update(contribution)

        self._update_person(
            person,
            first_name=contribution.first_name,
            last_name=contribution.last_name,
            sex=contribution.sex,
            birth_date=contribution.birth_date,
            death_date=contribution.death_date,
        )
        await self._person_gateway.update(person)

        return achievement.id if achievement else None


class LoggingProcessor:
    def __init__(self, processor: TransactionProcessor):
        self._processor = processor

    async def process(
        self,
        command: AcceptPersonEditingCommand,
    ) -> Optional[AchievementId]:
        command_processing_id = uuid7()

        logger.debug(
            "'Accept Person Editing' command processing started",
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
        except PersonDoesNotExistError as e:
            logger.error(
                "Unexpected error occurred: Contribution has person id,"
                "using which person gateway returns None",
                extra={"processing_id": command_processing_id},
            )
            raise e
        except InvalidPersonFirstNameError as e:
            logger.error(
                "Unexpected error occurred: Invalid person first name",
                extra={"processing_id": command_processing_id},
            )
            raise e
        except InvalidPersonLastNameError as e:
            logger.error(
                "Unexpected error occurred: Invalid person last name",
                extra={"processing_id": command_processing_id},
            )
            raise e
        except InvalidPersonBirthOrDeathDateError as e:
            logger.error(
                "Unexpected error occurred: Invalid person birth or death date",
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
            "'Accept Person Editing' command processing completed",
            extra={
                "processing_id": command_processing_id,
                "achievement_id": result,
            },
        )

        return result
