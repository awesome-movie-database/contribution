import logging
from datetime import datetime, timezone

from uuid_extensions import uuid7

from contribution.domain.value_objects import EditPersonContributionId
from contribution.domain.services import EditPerson
from contribution.application.common.services import (
    AccessConcern,
    CreatePhotoFromObj,
)
from contribution.application.common.command_processors import (
    CommandProcessor,
    AuthorizationProcessor,
    TransactionProcessor,
)
from contribution.application.common.exceptions import (
    UserDoesNotExistError,
    PersonDoesNotExistError,
)
from contribution.application.common.gateways import (
    EditPersonContributionGateway,
    UserGateway,
    PersonGateway,
    PermissionsGateway,
)
from contribution.application.common.object_storage import ObjectStorage
from contribution.application.common.unit_of_work import UnitOfWork
from contribution.application.common.identity_provider import IdentityProvider
from contribution.application.common.callbacks import OnPersonEdited
from contribution.application.commands import EditPersonCommand


logger = logging.getLogger(__name__)


def edit_person_factory(
    edit_person: EditPerson,
    access_concern: AccessConcern,
    create_photo_from_obj: CreatePhotoFromObj,
    edit_person_contribution_gateway: EditPersonContributionGateway,
    user_gateway: UserGateway,
    person_gateway: PersonGateway,
    permissions_gateway: PermissionsGateway,
    unit_of_work: UnitOfWork,
    object_storage: ObjectStorage,
    identity_provider: IdentityProvider,
    on_person_edited: OnPersonEdited,
) -> CommandProcessor[EditPersonCommand, EditPersonContributionId]:
    current_timestamp = datetime.now(timezone.utc)

    add_person_processor = EditPersonProcessor(
        edit_person=edit_person,
        create_photo_from_obj=create_photo_from_obj,
        edit_person_contribution_gateway=edit_person_contribution_gateway,
        user_gateway=user_gateway,
        person_gateway=person_gateway,
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
        on_person_edited=on_person_edited,
        identity_provider=identity_provider,
        current_timestamp=current_timestamp,
    )
    tx_processor = TransactionProcessor(
        processor=callback_processor,
        unit_of_work=unit_of_work,
    )
    log_processor = LoggingProcessor(
        processor=tx_processor,
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
        object_storage: ObjectStorage,
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
        self._object_storage = object_storage
        self._identity_provider = identity_provider
        self._current_timestamp = current_timestamp

    async def process(
        self,
        command: EditPersonCommand,
    ) -> EditPersonContributionId:
        current_user_id = await self._identity_provider.user_id()

        author = await self._user_gateway.with_id(current_user_id)
        if not author:
            raise UserDoesNotExistError(current_user_id)

        person = await self._person_gateway.with_id(command.person_id)
        if not person:
            raise PersonDoesNotExistError()

        photos = [
            self._create_photo_from_obj(obj) for obj in command.add_photos
        ]

        contribution = self._edit_person(
            id=EditPersonContributionId(uuid7()),
            author=author,
            person=person,
            first_name=command.first_name,
            last_name=command.last_name,
            birth_date=command.birth_date,
            death_date=command.death_date,
            current_timestamp=self._current_timestamp,
        )
        await self._edit_person_contribution_gateway.save(contribution)

        await self._object_storage.save_photo_seq(photos)

        return contribution.id


class CallbackProcessor:
    def __init__(
        self,
        *,
        processor: AuthorizationProcessor,
        on_person_edited: OnPersonEdited,
        identity_provider: IdentityProvider,
        current_timestamp: datetime,
    ):
        self._processor = processor
        self._on_person_edited = on_person_edited
        self._identity_provider = identity_provider
        self._current_timestamp = current_timestamp

    async def process(
        self,
        command: EditPersonCommand,
    ) -> EditPersonCommand:
        result = await self._processor.process(command)
        current_user_id = await self._identity_provider.user_id()

        await self._on_person_edited(
            id=result,
            author_id=current_user_id,
            person_id=command.person_id,
            first_name=command.first_name,
            last_name=command.last_name,
            birth_date=command.birth_date,
            death_date=command.death_date,
            edited_at=self._current_timestamp,
        )

        return result


class LoggingProcessor:
    def __init__(self, processor: TransactionProcessor):
        self._processor = processor

    async def process(
        self,
        command: EditPersonCommand,
    ) -> EditPersonContributionId:
        logger.debug(
            msg="Processing Edit Person command",
            extra={"command": command},
        )

        try:
            result = await self._processor.process(command)
        except UserDoesNotExistError as e:
            logger.error(
                msg="User is authenticated, but user gateway returns None",
                extra={"user_id": e.id},
            )
            raise e

        logger.debug(
            msg="Edit person command was processed",
            extra={"contribution_id": result},
        )

        return result
