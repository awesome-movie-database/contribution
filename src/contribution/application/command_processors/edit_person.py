import logging
from datetime import datetime, timezone

from uuid_extensions import uuid7

from contribution.domain import (
    EditPersonContributionId,
    EditPerson,
)
from contribution.application.common import (
    OperationId,
    AccessConcern,
    CreatePhotoFromObj,
    CommandProcessor,
    AuthorizationProcessor,
    TransactionProcessor,
    UserDoesNotExistError,
    PersonDoesNotExistError,
    NotEnoughPermissionsError,
    EditPersonContributionGateway,
    UserGateway,
    PersonGateway,
    PermissionsGateway,
    PhotoGateway,
    UnitOfWork,
    IdentityProvider,
    OnEventOccurred,
    PersonEditedEvent,
)
from contribution.application.commands import EditPersonCommand


logger = logging.getLogger(__name__)


def edit_person_factory(
    operation_id: OperationId,
    edit_person: EditPerson,
    access_concern: AccessConcern,
    create_photo_from_obj: CreatePhotoFromObj,
    edit_person_contribution_gateway: EditPersonContributionGateway,
    user_gateway: UserGateway,
    person_gateway: PersonGateway,
    permissions_gateway: PermissionsGateway,
    unit_of_work: UnitOfWork,
    photo_gateway: PhotoGateway,
    identity_provider: IdentityProvider,
    on_person_edited: OnEventOccurred[PersonEditedEvent],
) -> CommandProcessor[EditPersonCommand, EditPersonContributionId]:
    current_timestamp = datetime.now(timezone.utc)

    add_person_processor = EditPersonProcessor(
        edit_person=edit_person,
        create_photo_from_obj=create_photo_from_obj,
        edit_person_contribution_gateway=edit_person_contribution_gateway,
        user_gateway=user_gateway,
        person_gateway=person_gateway,
        photo_gateway=photo_gateway,
        identity_provider=identity_provider,
        current_timestamp=current_timestamp,
    )
    authz_processor = AuthorizationProcessor(
        processor=add_person_processor,
        access_concern=access_concern,
        permissions_gateway=permissions_gateway,
        identity_provider=identity_provider,
    )
    callback_processor = EditPersonCallbackProcessor(
        processor=authz_processor,
        create_photo_from_obj=create_photo_from_obj,
        identity_provider=identity_provider,
        on_person_edited=on_person_edited,
        current_timestamp=current_timestamp,
    )
    tx_processor = TransactionProcessor(
        processor=callback_processor,
        unit_of_work=unit_of_work,
    )
    log_processor = EditPersonLoggingProcessor(
        processor=tx_processor,
        operation_id=operation_id,
        identity_provider=identity_provider,
    )

    return log_processor


class EditPersonProcessor:
    def __init__(
        self,
        *,
        edit_person: EditPerson,
        create_photo_from_obj: CreatePhotoFromObj,
        edit_person_contribution_gateway: EditPersonContributionGateway,
        user_gateway: UserGateway,
        person_gateway: PersonGateway,
        photo_gateway: PhotoGateway,
        identity_provider: IdentityProvider,
        current_timestamp: datetime,
    ):
        self._edit_person = edit_person
        self._create_photo_from_obj = create_photo_from_obj
        self._edit_person_contribution_gateway = (
            edit_person_contribution_gateway
        )
        self._user_gateway = user_gateway
        self._person_gateway = person_gateway
        self._photo_gateway = photo_gateway
        self._identity_provider = identity_provider
        self._current_timestamp = current_timestamp

    async def process(
        self,
        command: EditPersonCommand,
    ) -> EditPersonContributionId:
        current_user_id = await self._identity_provider.user_id()

        author = await self._user_gateway.by_id(current_user_id)
        if not author:
            raise UserDoesNotExistError()

        person = await self._person_gateway.by_id(command.person_id)
        if not person:
            raise PersonDoesNotExistError()

        add_photos = [
            self._create_photo_from_obj(obj) for obj in command.add_photos
        ]

        contribution = self._edit_person(
            id=EditPersonContributionId(uuid7()),
            author=author,
            person=person,
            first_name=command.first_name,
            last_name=command.last_name,
            sex=command.sex,
            birth_date=command.birth_date,
            death_date=command.death_date,
            add_photos=[photo.url for photo in add_photos],
            current_timestamp=self._current_timestamp,
        )
        await self._edit_person_contribution_gateway.save(contribution)

        await self._photo_gateway.save_many(add_photos)

        return contribution.id


class EditPersonCallbackProcessor:
    def __init__(
        self,
        *,
        processor: AuthorizationProcessor,
        create_photo_from_obj: CreatePhotoFromObj,
        identity_provider: IdentityProvider,
        on_person_edited: OnEventOccurred[PersonEditedEvent],
        current_timestamp: datetime,
    ):
        self._processor = processor
        self._create_photo_from_obj = create_photo_from_obj
        self._identity_provider = identity_provider
        self._on_person_edited = on_person_edited
        self._current_timestamp = current_timestamp

    async def process(
        self,
        command: EditPersonCommand,
    ) -> EditPersonContributionId:
        result = await self._processor.process(command)
        current_user_id = await self._identity_provider.user_id()
        add_photos = [
            self._create_photo_from_obj(obj) for obj in command.add_photos
        ]

        event = PersonEditedEvent(
            contribution_id=result,
            author_id=current_user_id,
            person_id=command.person_id,
            first_name=command.first_name,
            sex=command.sex,
            last_name=command.last_name,
            birth_date=command.birth_date,
            death_date=command.death_date,
            add_photos=[photo.url for photo in add_photos],
            edited_at=self._current_timestamp,
        )
        await self._on_person_edited(event)

        return result


class EditPersonLoggingProcessor:
    def __init__(
        self,
        *,
        processor: TransactionProcessor,
        operation_id: OperationId,
        identity_provider: IdentityProvider,
    ):
        self._processor = processor
        self._operation_id = operation_id
        self._identity_provider = identity_provider

    async def process(
        self,
        command: EditPersonCommand,
    ) -> EditPersonContributionId:
        current_user_id = await self._identity_provider.user_id()

        logger.debug(
            "'Edit Person' command processing started",
            extra={
                "operation_id": self._operation_id,
                "user_id": current_user_id,
                "command": command,
            },
        )

        try:
            result = await self._processor.process(command)
        except NotEnoughPermissionsError as e:
            logger.debug(
                "Expected error occurred: User has not enough permissions",
                extra={
                    "operation_id": self._operation_id,
                    "current_user_permissions": (
                        await self._identity_provider.permissions(),
                    ),
                },
            )
            raise e
        except UserDoesNotExistError as e:
            logger.error(
                "Unexpected error occurred: "
                "User is authenticated, but user gateway returns None",
                extra={"operation_id": self._operation_id},
            )
            raise e
        except PersonDoesNotExistError as e:
            logger.error(
                "Unexpected error occurred: Person doesn't exist",
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
            "'Edit Person' command processing completed",
            extra={
                "operation_id": self._operation_id,
                "contribution_id": result,
            },
        )

        return result
