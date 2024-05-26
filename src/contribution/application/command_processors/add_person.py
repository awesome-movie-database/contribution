import logging
from datetime import datetime, timezone

from uuid_extensions import uuid7

from contribution.domain import (
    AddPersonContributionId,
    UserIsNotActiveError,
    AddPerson,
)
from contribution.application.common import (
    AccessConcern,
    CreatePhotoFromObj,
    CommandProcessor,
    AuthorizationProcessor,
    TransactionProcessor,
    UserDoesNotExistError,
    NotEnoughPermissionsError,
    AddPersonContributionGateway,
    UserGateway,
    PermissionsGateway,
    ObjectStorage,
    UnitOfWork,
    IdentityProvider,
    OnEventOccurred,
    PersonAddedEvent,
)
from contribution.application.commands import AddPersonCommand


logger = logging.getLogger(__name__)


def add_person_factory(
    add_person: AddPerson,
    access_concern: AccessConcern,
    create_photo_from_obj: CreatePhotoFromObj,
    add_person_contribution_gateway: AddPersonContributionGateway,
    user_gateway: UserGateway,
    permissions_gateway: PermissionsGateway,
    unit_of_work: UnitOfWork,
    object_storage: ObjectStorage,
    identity_provider: IdentityProvider,
    on_person_added: OnEventOccurred[PersonAddedEvent],
) -> CommandProcessor[AddPersonCommand, AddPersonContributionId]:
    current_timestamp = datetime.now(timezone.utc)

    add_person_processor = AddPersonProcessor(
        add_person=add_person,
        create_photo_from_obj=create_photo_from_obj,
        add_person_contribution_gateway=add_person_contribution_gateway,
        user_gateway=user_gateway,
        object_storage=object_storage,
        identity_provider=identity_provider,
        current_timestamp=current_timestamp,
    )
    authz_processor = AuthorizationProcessor(
        processor=add_person_processor,
        access_concern=access_concern,
        permissions_gateway=permissions_gateway,
        identity_provider=identity_provider,
    )
    callback_processor = CallbackProcessor(
        processor=authz_processor,
        create_photo_from_obj=create_photo_from_obj,
        identity_provider=identity_provider,
        on_person_added=on_person_added,
        current_timestamp=current_timestamp,
    )
    tx_processor = TransactionProcessor(
        processor=callback_processor,
        unit_of_work=unit_of_work,
    )
    log_processor = LoggingProcessor(
        processor=tx_processor,
        identity_provider=identity_provider,
    )

    return log_processor


class AddPersonProcessor:
    def __init__(
        self,
        *,
        add_person: AddPerson,
        create_photo_from_obj: CreatePhotoFromObj,
        add_person_contribution_gateway: AddPersonContributionGateway,
        user_gateway: UserGateway,
        object_storage: ObjectStorage,
        identity_provider: IdentityProvider,
        current_timestamp: datetime,
    ):
        self._add_person = add_person
        self._create_photo_from_obj = create_photo_from_obj
        self._add_person_contribution_gateway = add_person_contribution_gateway
        self._user_gateway = user_gateway
        self._object_storage = object_storage
        self._identity_provider = identity_provider
        self._current_timestamp = current_timestamp

    async def process(
        self,
        command: AddPersonCommand,
    ) -> AddPersonContributionId:
        current_user_id = await self._identity_provider.user_id()

        author = await self._user_gateway.by_id(current_user_id)
        if not author:
            raise UserDoesNotExistError()

        photos = [self._create_photo_from_obj(obj) for obj in command.photos]

        contribution = self._add_person(
            id=AddPersonContributionId(uuid7()),
            author=author,
            first_name=command.first_name,
            last_name=command.last_name,
            sex=command.sex,
            birth_date=command.birth_date,
            death_date=command.death_date,
            photos=[photo.url for photo in photos],
            current_timestamp=self._current_timestamp,
        )
        await self._add_person_contribution_gateway.save(contribution)

        await self._object_storage.save_photos(photos)

        return contribution.id


class CallbackProcessor:
    def __init__(
        self,
        *,
        processor: AuthorizationProcessor,
        create_photo_from_obj: CreatePhotoFromObj,
        identity_provider: IdentityProvider,
        on_person_added: OnEventOccurred[PersonAddedEvent],
        current_timestamp: datetime,
    ):
        self._processor = processor
        self._create_photo_from_obj = create_photo_from_obj
        self._identity_provider = identity_provider
        self._on_person_added = on_person_added
        self._current_timestamp = current_timestamp

    async def process(
        self,
        command: AddPersonCommand,
    ) -> AddPersonContributionId:
        result = await self._processor.process(command)
        current_user_id = await self._identity_provider.user_id()
        photos = [self._create_photo_from_obj(obj) for obj in command.photos]

        event = PersonAddedEvent(
            contribtion_id=result,
            author_id=current_user_id,
            first_name=command.first_name,
            last_name=command.last_name,
            sex=command.sex,
            birth_date=command.birth_date,
            death_date=command.death_date,
            photos=[photo.url for photo in photos],
            added_at=self._current_timestamp,
        )
        await self._on_person_added(event)

        return result


class LoggingProcessor:
    def __init__(
        self,
        *,
        processor: TransactionProcessor,
        identity_provider: IdentityProvider,
    ):
        self._processor = processor
        self._identity_provider = identity_provider

    async def process(
        self,
        command: AddPersonCommand,
    ) -> AddPersonContributionId:
        current_user_id = await self._identity_provider.user_id()
        command_processing_id = uuid7()

        logger.debug(
            msg="'Add Person' command processing started",
            extra={
                "processing_id": command_processing_id,
                "command": command,
                "current_user_id": current_user_id,
            },
        )

        try:
            result = await self._processor.process(command)
        except NotEnoughPermissionsError as e:
            logger.debug(
                "Expected error occurred: User has not enough permissions",
                extra={
                    "processing_id": command_processing_id,
                    "current_user_permissions": (
                        await self._identity_provider.permissions(),
                    ),
                },
            )
            raise e
        except UserDoesNotExistError as e:
            logger.warning(
                "Unexpected error occurred: "
                "User is authenticated, but user gateway returns None",
                extra={"processing_id": command_processing_id},
            )
            raise e
        except UserIsNotActiveError as e:
            logger.debug(
                "Expected error occurred: User is not active",
                extra={"processing_id": command_processing_id},
            )
            raise e
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
            msg="'Add Person' command processing completed",
            extra={
                "processing_id": command_processing_id,
                "contribution_id": result,
            },
        )

        return result
