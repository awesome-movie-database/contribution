import logging

from uuid_extensions import uuid7

from contribution.domain.value_objects import AchievementId
from contribution.domain.services import (
    AcceptContribution,
    CreatePerson,
)
from contribution.application.common.command_processors import (
    CommandProcessor,
    TransactionProcessor,
)
from contribution.application.common.exceptions import (
    PersonIdIsAlreadyTakenError,
    UserDoesNotExistError,
    ContributionDoesNotExistError,
)
from contribution.application.common.gateways import (
    AddPersonContributionGateway,
    PersonGateway,
    UserGateway,
    AchievementGateway,
)
from contribution.application.common.unit_of_work import UnitOfWork
from contribution.application.common.callbacks import OnAchievementEarned
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
    on_achievement_earned: OnAchievementEarned,
) -> CommandProcessor[AcceptPersonAdditionCommand, None]:
    accept_person_addition_processor = AcceptPersonAdditionProcessor(
        accept_contribution=accept_contribution,
        create_person=create_person,
        add_person_contribution_gateway=add_person_contribution_gateway,
        user_gateway=user_gateway,
        person_gateway=person_gateway,
        achievement_gateway=achievement_gateway,
        on_achievement_earned=on_achievement_earned,
    )
    tx_processor = TransactionProcessor(
        processor=accept_person_addition_processor,
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
        on_achievement_earned: OnAchievementEarned,
    ):
        self._accept_contribution = accept_contribution
        self._create_person = create_person
        self._add_person_contribution_gateway = add_person_contribution_gateway
        self._user_gateway = user_gateway
        self._person_gateway = person_gateway
        self._achievement_gateway = achievement_gateway
        self._on_achievement_earned = on_achievement_earned

    async def process(
        self,
        command: AcceptPersonAdditionCommand,
    ) -> None:
        contribution = await self._add_person_contribution_gateway.with_id(
            id=command.contribution_id,
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

        if achievement:
            await self._on_achievement_earned(
                id=achievement.id,
                user_id=achievement.user_id,
                achieved=achievement.achieved,
                achieved_at=command.accepted_at,
            )


class LoggingProcessor:
    def __init__(self, processor: TransactionProcessor):
        self._processor = processor

    async def process(
        self,
        command: AcceptPersonAdditionCommand,
    ) -> None:
        logger.debug(
            msg="Processing Accept Person Addition command",
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
        except PersonIdIsAlreadyTakenError as e:
            logger.error(
                msg="Person id is already taken",
                extra={"person_id": command.person_id},
            )
            raise e

        logger.debug(
            msg="Accept Person Addition command was processed",
        )

        return result
