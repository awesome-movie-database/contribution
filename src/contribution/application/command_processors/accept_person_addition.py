import logging
from typing import Optional

from uuid_extensions import uuid7

from contribution.domain import (
    AchievementId,
    InvalidPersonFirstNameError,
    InvalidPersonLastNameError,
    InvalidPersonBirthOrDeathDateError,
    AcceptContribution,
    CreatePerson,
)
from contribution.application.common import (
    CommandProcessor,
    TransactionProcessor,
    AchievementEearnedCallbackProcessor,
    PersonIdIsAlreadyTakenError,
    UserDoesNotExistError,
    ContributionDoesNotExistError,
    AchievementDoesNotExistError,
    AddPersonContributionGateway,
    PersonGateway,
    UserGateway,
    AchievementGateway,
    UnitOfWork,
    OnEventOccurred,
    AchievementEarnedEvent,
)
from contribution.application.commands import AcceptPersonAdditionCommand


logger = logging.getLogger(__name__)


def accept_person_addition_factory(
    accept_contribution: AcceptContribution,
    create_person: CreatePerson,
    add_person_contribution_gateway: AddPersonContributionGateway,
    user_gateway: UserGateway,
    person_gateway: PersonGateway,
    achievement_gateway: AchievementGateway,
    unit_of_work: UnitOfWork,
    on_achievement_earned: OnEventOccurred[AchievementEarnedEvent],
) -> CommandProcessor[AcceptPersonAdditionCommand, Optional[AchievementId]]:
    accept_person_addition_processor = AcceptPersonAdditionProcessor(
        accept_contribution=accept_contribution,
        create_person=create_person,
        add_person_contribution_gateway=add_person_contribution_gateway,
        user_gateway=user_gateway,
        person_gateway=person_gateway,
        achievement_gateway=achievement_gateway,
    )
    callback_processor = AchievementEearnedCallbackProcessor(
        processor=accept_person_addition_processor,
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


class AcceptPersonAdditionProcessor:
    def __init__(
        self,
        *,
        accept_contribution: AcceptContribution,
        create_person: CreatePerson,
        add_person_contribution_gateway: AddPersonContributionGateway,
        user_gateway: UserGateway,
        person_gateway: PersonGateway,
        achievement_gateway: AchievementGateway,
    ):
        self._accept_contribution = accept_contribution
        self._create_person = create_person
        self._add_person_contribution_gateway = add_person_contribution_gateway
        self._user_gateway = user_gateway
        self._person_gateway = person_gateway
        self._achievement_gateway = achievement_gateway

    async def process(
        self,
        command: AcceptPersonAdditionCommand,
    ) -> Optional[AchievementId]:
        contribution = (
            await self._add_person_contribution_gateway.acquire_with_id(
                id=command.contribution_id,
            )
        )
        if not contribution:
            raise ContributionDoesNotExistError()

        author = await self._user_gateway.acquire_with_id(
            id=contribution.author_id,
        )
        if not author:
            raise UserDoesNotExistError(contribution.author_id)

        person = await self._person_gateway.with_id(command.person_id)
        if person:
            raise PersonIdIsAlreadyTakenError()

        achievement = self._accept_contribution(
            achievement_id=AchievementId(uuid7()),
            contribution=contribution,
            author=author,
            current_timestamp=command.accepted_at,
        )
        if achievement:
            await self._achievement_gateway.save(achievement)

        await self._user_gateway.update(author)
        await self._add_person_contribution_gateway.update(contribution)

        new_person = self._create_person(
            id=command.person_id,
            first_name=contribution.first_name,
            last_name=contribution.last_name,
            sex=contribution.sex,
            birth_date=contribution.birth_date,
            death_date=contribution.death_date,
        )
        await self._person_gateway.save(new_person)

        return achievement.id if achievement else None


class LoggingProcessor:
    def __init__(self, processor: TransactionProcessor):
        self._processor = processor

    async def process(
        self,
        command: AcceptPersonAdditionCommand,
    ) -> Optional[AchievementId]:
        command_processing_id = uuid7()

        logger.debug(
            msg="'Accept Person Addition' command processing started",
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
        except PersonIdIsAlreadyTakenError as e:
            logger.error(
                "Unexpected error occurred: Person id is already taken",
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
            "'Accept Person Addition' command processing completed",
            extra={
                "processing_id": command_processing_id,
                "achievement_id": result,
            },
        )

        return result
