import logging
from datetime import datetime, timezone

from uuid_extensions import uuid7

from contribution.domain.value_objects import AchievementId
from contribution.domain.services import (
    AcceptContribution,
    UpdatePerson,
)
from contribution.application.common.command_processors import (
    CommandProcessor,
    TransactionProcessor,
)
from contribution.application.common.exceptions import (
    PersonDoesNotExistError,
    UserDoesNotExistError,
    ContributionDoesNotExistError,
)
from contribution.application.common.gateways import (
    EditPersonContributionGateway,
    PersonGateway,
    UserGateway,
    AchievementGateway,
)
from contribution.application.common.unit_of_work import UnitOfWork
from contribution.application.common.callbacks import (
    OnAchievementEarned,
    OnPersonEditingAccepted,
)
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
    on_achievement_earned: OnAchievementEarned,
    on_person_editing_accepted: OnPersonEditingAccepted,
) -> CommandProcessor[AcceptPersonEditingCommand, None]:
    accept_person_editing_processor = AcceptPersonEditingProcessor(
        accept_contribution=accept_contribution,
        update_person=update_person,
        edit_person_contribution_gateway=edit_person_contribution_gateway,
        user_gateway=user_gateway,
        person_gateway=person_gateway,
        achievement_gateway=achievement_gateway,
        on_achievement_earned=on_achievement_earned,
        on_person_editing_accepted=on_person_editing_accepted,
    )
    tx_processor = TransactionProcessor(
        processor=accept_person_editing_processor,
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
        on_achievement_earned: OnAchievementEarned,
        on_person_editing_accepted: OnPersonEditingAccepted,
    ):
        self._accept_contribution = accept_contribution
        self._update_person = update_person
        self._edit_person_contribution_gateway = (
            edit_person_contribution_gateway
        )
        self._user_gateway = user_gateway
        self._person_gateway = person_gateway
        self._achievement_gateway = achievement_gateway
        self._on_achievement_earned = on_achievement_earned
        self._on_person_editing_accepted = on_person_editing_accepted

    async def process(
        self,
        command: AcceptPersonEditingCommand,
    ) -> None:
        current_timestamp = datetime.now(timezone.utc)

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
            current_timestamp=current_timestamp,
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

        await self._on_person_editing_accepted(
            id=contribution.id,
            accepted_at=current_timestamp,
        )

        if achievement:
            await self._on_achievement_earned(
                id=achievement.id,
                user_id=achievement.user_id,
                achieved=achievement.achieved,
                achieved_at=current_timestamp,
            )


class LoggingProcessor:
    def __init__(self, processor: TransactionProcessor):
        self._processor = processor

    async def process(
        self,
        command: AcceptPersonEditingCommand,
    ) -> None:
        logger.debug(
            msg="Processing Accept Person Editing command",
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
            msg="Accept Person Editing command was processed",
        )

        return result
