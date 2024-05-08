import logging
from datetime import datetime, timezone

from uuid_extensions import uuid7

from contribution.domain.value_objects import AddMovieContributionId
from contribution.domain.exceptions import (
    UserIsNotActiveError,
    InvalidMovieEngTitleError,
    InvalidMovieOriginalTitleError,
    InvalidMovieDurationError,
)
from contribution.domain.services import AddMovie
from contribution.application.common.services import (
    AccessConcern,
    EnsurePersonsExist,
    CreatePhotoFromObj,
)
from contribution.application.common.command_processors import (
    CommandProcessor,
    AuthorizationProcessor,
    TransactionProcessor,
)
from contribution.application.common.exceptions import (
    UserDoesNotExistError,
    PersonsDoNotExistError,
    NotEnoughPermissionsError,
)
from contribution.application.common.gateways import (
    AddMovieContributionGateway,
    UserGateway,
    PermissionsGateway,
)
from contribution.application.common.object_storage import ObjectStorage
from contribution.application.common.unit_of_work import UnitOfWork
from contribution.application.common.identity_provider import IdentityProvider
from contribution.application.common.callbacks import OnMovieAdded
from contribution.application.commands import AddMovieCommand


logger = logging.getLogger(__name__)


def add_movie_factory(
    add_movie: AddMovie,
    access_concern: AccessConcern,
    ensure_persons_exist: EnsurePersonsExist,
    create_photo_from_obj: CreatePhotoFromObj,
    add_movie_contribution_gateway: AddMovieContributionGateway,
    user_gateway: UserGateway,
    permissions_gateway: PermissionsGateway,
    object_storage: ObjectStorage,
    unit_of_work: UnitOfWork,
    identity_provider: IdentityProvider,
    on_movie_added: OnMovieAdded,
) -> CommandProcessor[AddMovieCommand, AddMovieContributionId]:
    current_timestamp = datetime.now(timezone.utc)

    add_movie_processor = AddMovieProcessor(
        add_movie=add_movie,
        ensure_persons_exist=ensure_persons_exist,
        create_photo_from_obj=create_photo_from_obj,
        add_movie_contribution_gateway=add_movie_contribution_gateway,
        user_gateway=user_gateway,
        object_storage=object_storage,
        identity_provider=identity_provider,
        current_timestamp=current_timestamp,
    )
    authz_processor = AuthorizationProcessor(
        processor=add_movie_processor,
        access_concern=access_concern,
        permissions_gateway=permissions_gateway,
        identity_provider=identity_provider,
    )
    callback_processor = CallbackProcessor(
        processor=authz_processor,
        create_photo_from_obj=create_photo_from_obj,
        identity_provider=identity_provider,
        on_movie_added=on_movie_added,
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


class AddMovieProcessor:
    def __init__(
        self,
        *,
        add_movie: AddMovie,
        ensure_persons_exist: EnsurePersonsExist,
        create_photo_from_obj: CreatePhotoFromObj,
        add_movie_contribution_gateway: AddMovieContributionGateway,
        user_gateway: UserGateway,
        object_storage: ObjectStorage,
        identity_provider: IdentityProvider,
        current_timestamp: datetime,
    ):
        self._add_movie = add_movie
        self._ensure_persons_exist = ensure_persons_exist
        self._create_photo_from_obj = create_photo_from_obj
        self._add_movie_contribution_gateway = add_movie_contribution_gateway
        self._user_gateway = user_gateway
        self._object_storage = object_storage
        self._identity_provider = identity_provider
        self._current_timestamp = current_timestamp

    async def process(
        self,
        command: AddMovieCommand,
    ) -> AddMovieContributionId:
        current_user_id = await self._identity_provider.user_id()

        author = await self._user_gateway.with_id(current_user_id)
        if not author:
            raise UserDoesNotExistError(current_user_id)

        await self._ensure_persons_exist(
            *(role.person_id for role in command.roles),
            *(writer.person_id for writer in command.writers),
            *(crew_member.person_id for crew_member in command.crew),
        )

        photos = [self._create_photo_from_obj(obj) for obj in command.photos]

        contribution = self._add_movie(
            id=AddMovieContributionId(uuid7()),
            author=author,
            eng_title=command.eng_title,
            original_title=command.original_title,
            release_date=command.release_date,
            countries=command.countries,
            genres=command.genres,
            mpaa=command.mpaa,
            duration=command.duration,
            budget=command.budget,
            revenue=command.revenue,
            roles=command.roles,
            writers=command.writers,
            crew=command.crew,
            photos=[photo.url for photo in photos],
            current_timestamp=self._current_timestamp,
        )
        await self._add_movie_contribution_gateway.save(contribution)

        await self._object_storage.save_photo_seq(photos)

        return contribution.id


class CallbackProcessor:
    def __init__(
        self,
        *,
        processor: AuthorizationProcessor,
        create_photo_from_obj: CreatePhotoFromObj,
        identity_provider: IdentityProvider,
        on_movie_added: OnMovieAdded,
        current_timestamp: datetime,
    ):
        self._processor = processor
        self._create_photo_from_obj = create_photo_from_obj
        self._identity_provider = identity_provider
        self._on_movie_added = on_movie_added
        self._current_timestamp = current_timestamp

    async def process(
        self,
        command: AddMovieCommand,
    ) -> AddMovieContributionId:
        result = await self._processor.process(command)
        current_user_id = await self._identity_provider.user_id()
        photos = [self._create_photo_from_obj(obj) for obj in command.photos]

        await self._on_movie_added(
            id=result,
            author_id=current_user_id,
            eng_title=command.eng_title,
            original_title=command.original_title,
            release_date=command.release_date,
            countries=command.countries,
            genres=command.genres,
            mpaa=command.mpaa,
            duration=command.duration,
            budget=command.budget,
            revenue=command.revenue,
            roles=command.roles,
            writers=command.writers,
            crew=command.crew,
            photos=[photo.url for photo in photos],
            added_at=self._current_timestamp,
        )

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
        command: AddMovieCommand,
    ) -> AddMovieContributionId:
        current_user_id = await self._identity_provider.user_id()
        command_processing_id = uuid7()

        logger.debug(
            "'Add Movie' command processing started",
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
        except PersonsDoNotExistError as e:
            logger.debug(
                "Expected error occurred: "
                "Person ids entered by user do not belong to any persons",
                extra={
                    "processing_id": command_processing_id,
                    "ids_of_missing_persons": e.ids_of_missing_persons,
                },
            )
            raise e
        except InvalidMovieEngTitleError as e:
            logger.error(
                "Unexpected error occurred: Invalid movie eng title",
                extra={"processing_id": command_processing_id},
            )
            raise e
        except InvalidMovieOriginalTitleError as e:
            logger.error(
                "Unexpected error occurred: Invalid movie original title",
                extra={"processing_id": command_processing_id},
            )
            raise e
        except InvalidMovieDurationError as e:
            logger.error(
                "Unexpected error occurred: Invalid movie duration",
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
            "'Add Movie' command processing completed",
            extra={
                "processing_id": command_processing_id,
                "contribution_id": result,
            },
        )

        return result
