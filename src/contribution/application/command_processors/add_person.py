import logging
from datetime import datetime, timezone

from uuid_extensions import uuid7

from contribution.domain.value_objects import AddPersonContributionId
from contribution.domain.services import AddPerson
from contribution.application.common.services import (
    AccessConcern,
    CreatePhotoFromObj,
)
from contribution.application.common.command_processors import (
    CommandProcessor,
    AuthorizationProcessor,
    TransactionProcessor,
)
from contribution.application.common.exceptions import UserDoesNotExistError
from contribution.application.common.gateways import (
    AddPersonContributionGateway,
    UserGateway,
    PermissionsGateway,
)
from contribution.application.common.object_storage import ObjectStorage
from contribution.application.common.unit_of_work import UnitOfWork
from contribution.application.common.identity_provider import IdentityProvider
from contribution.application.common.callbacks import OnPersonAdded
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
    on_person_added: OnPersonAdded,
) -> CommandProcessor[AddPersonCommand, AddPersonContributionId]:
    add_person_processor = AddPersonProcessor(
        add_person=add_person,
        create_photo_from_obj=create_photo_from_obj,
        add_person_contribution_gateway=add_person_contribution_gateway,
        user_gateway=user_gateway,
        object_storage=object_storage,
        identity_provider=identity_provider,
        on_person_added=on_person_added,
    )
    authz_processor = AuthorizationProcessor(
        processor=add_person_processor,
        access_concern=access_concern,
        permissions_gateway=permissions_gateway,
        identity_provider=identity_provider,
    )
    tx_processor = TransactionProcessor(
        processor=authz_processor,
        unit_of_work=unit_of_work,
    )
    log_processor = LoggingProcessor(
        processor=tx_processor,
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
        on_person_added: OnPersonAdded,
    ):
        self._add_person = add_person
        self._create_photo_from_obj = create_photo_from_obj
        self._add_person_contribution_gateway = add_person_contribution_gateway
        self._user_gateway = user_gateway
        self._object_storage = object_storage
        self._identity_provider = identity_provider
        self._on_person_added = on_person_added

    async def process(
        self,
        command: AddPersonCommand,
    ) -> AddPersonContributionId:
        current_user_id = await self._identity_provider.user_id()
        current_timestamp = datetime.now(timezone.utc)

        author = await self._user_gateway.with_id(current_user_id)
        if not author:
            raise UserDoesNotExistError(current_user_id)

        photos = [self._create_photo_from_obj(obj) for obj in command.photos]
        photos_urls = [photo.url for photo in photos]

        contribution = self._add_person(
            id=AddPersonContributionId(uuid7()),
            author=author,
            first_name=command.first_name,
            last_name=command.last_name,
            birth_date=command.birth_date,
            death_date=command.death_date,
            photos=photos_urls,
            current_timestamp=current_timestamp,
        )
        await self._add_person_contribution_gateway.save(contribution)

        await self._object_storage.save_photo_seq(photos)

        await self._on_person_added(
            id=contribution.id,
            author_id=current_user_id,
            first_name=command.first_name,
            last_name=command.last_name,
            birth_date=command.birth_date,
            death_date=command.death_date,
            photos=photos_urls,
            added_at=current_timestamp,
        )

        return contribution.id


class LoggingProcessor:
    def __init__(self, processor: TransactionProcessor):
        self._processor = processor

    async def process(
        self,
        command: AddPersonCommand,
    ) -> AddPersonContributionId:
        logger.debug(
            msg="Processing Add Person command",
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
            msg="Add person command was processed",
            extra={"contribution_id": result},
        )

        return result
