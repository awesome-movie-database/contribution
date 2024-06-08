import logging

from contribution.domain import (
    InvalidPersonFirstNameError,
    InvalidPersonLastNameError,
    InvalidPersonBirthOrDeathDateError,
    CreatePerson,
)
from contribution.application.common import (
    OperationId,
    CommandProcessor,
    TransactionProcessor,
    PersonIdIsAlreadyTakenError,
    PersonGateway,
    UnitOfWork,
)
from contribution.application.commands import CreatePersonCommand


logger = logging.getLogger(__name__)


def create_person_factory(
    operation_id: OperationId,
    create_person: CreatePerson,
    person_gateway: PersonGateway,
    unit_of_work: UnitOfWork,
) -> CommandProcessor[CreatePersonCommand, None]:
    create_person_processor = CreatePersonProcessor(
        create_person=create_person,
        person_gateway=person_gateway,
    )
    tx_processor = TransactionProcessor(
        processor=create_person_processor,
        unit_of_work=unit_of_work,
    )
    log_processor = LoggingProcessor(
        processor=tx_processor,
        operation_id=operation_id,
    )

    return log_processor


class CreatePersonProcessor:
    def __init__(
        self,
        *,
        create_person: CreatePerson,
        person_gateway: PersonGateway,
    ):
        self._create_person = create_person
        self._person_gateway = person_gateway

    async def process(self, command: CreatePersonCommand) -> None:
        person = await self._person_gateway.by_id(command.id)
        if person:
            raise PersonIdIsAlreadyTakenError()

        new_person = self._create_person(
            id=command.id,
            first_name=command.first_name,
            last_name=command.last_name,
            sex=command.sex,
            birth_date=command.birth_date,
            death_date=command.death_date,
        )
        await self._person_gateway.save(new_person)


class LoggingProcessor:
    def __init__(
        self,
        *,
        processor: TransactionProcessor,
        operation_id: OperationId,
    ):
        self._processor = processor
        self._operation_id = operation_id

    async def process(self, command: CreatePersonCommand) -> None:
        logger.debug(
            msg="'Create Person' command processing started",
            extra={
                "operation_id": self._operation_id,
                "command": command,
            },
        )

        try:
            result = await self._processor.process(command)
        except PersonIdIsAlreadyTakenError as e:
            logger.error(
                "Unexpected error occurred: Person id is already taken",
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
        except Exception as e:
            logger.exception(
                "Unexpected error occurred",
                exc_info=e,
                extra={
                    "operation_id": self._operation_id,
                    "error": e,
                },
            )
            raise e

        logger.debug(
            "'Create Person' command processing completed",
            extra={"operation_id": self._operation_id},
        )

        return result
