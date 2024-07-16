import logging

from contribution.domain import (
    InvalidPersonFirstNameError,
    InvalidPersonLastNameError,
    InvalidPersonBirthOrDeathDateError,
    UpdatePerson,
)
from contribution.application.common import (
    OperationId,
    CommandProcessor,
    TransactionProcessor,
    PersonDoesNotExistError,
    PersonGateway,
    UnitOfWork,
)
from contribution.application.commands import UpdatePersonCommand


logger = logging.getLogger(__name__)


def update_person_factory(
    operation_id: OperationId,
    update_person: UpdatePerson,
    person_gateway: PersonGateway,
    unit_of_work: UnitOfWork,
) -> CommandProcessor[UpdatePersonCommand, None]:
    update_person_processor = UpdatePersonProcessor(
        update_person=update_person,
        person_gateway=person_gateway,
    )
    tx_processor = TransactionProcessor(
        processor=update_person_processor,
        unit_of_work=unit_of_work,
    )
    log_processor = UpdatePersonLoggingProcessor(
        processor=tx_processor,
        operation_id=operation_id,
    )

    return log_processor


class UpdatePersonProcessor:
    def __init__(
        self,
        *,
        update_person: UpdatePerson,
        person_gateway: PersonGateway,
    ):
        self._update_person = update_person
        self._person_gateway = person_gateway

    async def process(self, command: UpdatePersonCommand) -> None:
        person = await self._person_gateway.acquire_by_id(command.person_id)
        if not person:
            raise PersonDoesNotExistError()

        self._update_person(
            person,
            first_name=command.first_name,
            last_name=command.last_name,
            sex=command.sex,
            birth_date=command.birth_date,
            death_date=command.death_date,
        )
        await self._person_gateway.update(person)


class UpdatePersonLoggingProcessor:
    def __init__(
        self,
        *,
        processor: TransactionProcessor,
        operation_id: OperationId,
    ):
        self._processor = processor
        self._operation_id = operation_id

    async def process(self, command: UpdatePersonCommand) -> None:
        logger.debug(
            msg="'Update Person' command processing started",
            extra={
                "operation_id": self._operation_id,
                "command": command,
            },
        )

        try:
            result = await self._processor.process(command)
        except PersonDoesNotExistError as e:
            logger.error(
                "Unexpected error occurred: Person doesn't exist",
                extra={"operation_id": self._operation_id},
            )
            raise e
        except InvalidPersonFirstNameError as e:
            logger.error(
                "Unexpected error occurred: Invalid person first name",
                extra={"operation_id": self._operation_id},
            )
            raise e
        except InvalidPersonLastNameError as e:
            logger.error(
                "Unexpected error occurred: Invalid person last name",
                extra={"operation_id": self._operation_id},
            )
            raise e
        except InvalidPersonBirthOrDeathDateError as e:
            logger.error(
                "Unexpected error occurred: Invalid person birth or death date",
                extra={"operation_id": self._operation_id},
            )
            raise e
        except Exception:
            logger.exception(
                "Unexpected error occurred",
                extra={"operation_id": self._operation_id},
            )
            raise e

        logger.debug(
            "'Update Person' command processing completed",
            extra={"operation_id": self._operation_id},
        )

        return result
