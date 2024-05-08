import logging
from datetime import datetime, timezone
from typing import Sequence

from uuid_extensions import uuid7

from contribution.domain.value_objects import (
    EditMovieContributionId,
    RoleId,
    WriterId,
    CrewMemberId,
)
from contribution.domain.exceptions import (
    UserIsNotActiveError,
    InvalidMovieEngTitleError,
    InvalidMovieOriginalTitleError,
    InvalidMovieDurationError,
)
from contribution.domain.services import EditMovie
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
    MovieDoesNotExistError,
    RolesDoNotExistError,
    WritersDoNotExistError,
    CrewMembersDoNotExistError,
    PersonsDoNotExistError,
    NotEnoughPermissionsError,
)
from contribution.application.common.gateways import (
    EditMovieContributionGateway,
    MovieGateway,
    UserGateway,
    RoleGateway,
    WriterGateway,
    CrewMemberGateway,
    PermissionsGateway,
)
from contribution.application.common.object_storage import ObjectStorage
from contribution.application.common.unit_of_work import UnitOfWork
from contribution.application.common.identity_provider import IdentityProvider
from contribution.application.common.callbacks import OnMovieEdited
from contribution.application.commands import EditMovieCommand


logger = logging.getLogger(__name__)


def edit_movie_factory(
    edit_movie: EditMovie,
    access_concern: AccessConcern,
    ensure_persons_exist: EnsurePersonsExist,
    create_photo_from_obj: CreatePhotoFromObj,
    edit_movie_contribution_gateway: EditMovieContributionGateway,
    user_gateway: UserGateway,
    movie_gateway: MovieGateway,
    role_gateway: RoleGateway,
    writer_gateway: WriterGateway,
    crew_member_gateway: CrewMemberGateway,
    permissions_gateway: PermissionsGateway,
    object_storage: ObjectStorage,
    unit_of_work: UnitOfWork,
    identity_provider: IdentityProvider,
    on_movie_edited: OnMovieEdited,
) -> CommandProcessor[EditMovieCommand, EditMovieContributionId]:
    current_timestamp = datetime.now(timezone.utc)

    edit_movie_processor = EditMovieProcessor(
        edit_movie=edit_movie,
        ensure_persons_exist=ensure_persons_exist,
        create_photo_from_obj=create_photo_from_obj,
        edit_movie_contribution_gateway=edit_movie_contribution_gateway,
        user_gateway=user_gateway,
        movie_gateway=movie_gateway,
        role_gateway=role_gateway,
        writer_gateway=writer_gateway,
        crew_member_gateway=crew_member_gateway,
        object_storage=object_storage,
        identity_provider=identity_provider,
        current_timestamp=current_timestamp,
    )
    authz_processor = AuthorizationProcessor(
        processor=edit_movie_processor,
        access_concern=access_concern,
        permissions_gateway=permissions_gateway,
        identity_provider=identity_provider,
    )
    callback_processor = CallbackProcessor(
        processor=authz_processor,
        create_photo_from_obj=create_photo_from_obj,
        identity_provider=identity_provider,
        on_movie_edited=on_movie_edited,
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


class EditMovieProcessor:
    def __init__(
        self,
        *,
        edit_movie: EditMovie,
        ensure_persons_exist: EnsurePersonsExist,
        create_photo_from_obj: CreatePhotoFromObj,
        edit_movie_contribution_gateway: EditMovieContributionGateway,
        user_gateway: UserGateway,
        movie_gateway: MovieGateway,
        role_gateway: RoleGateway,
        writer_gateway: WriterGateway,
        crew_member_gateway: CrewMemberGateway,
        object_storage: ObjectStorage,
        identity_provider: IdentityProvider,
        current_timestamp: datetime,
    ):
        self._edit_movie = edit_movie
        self._ensure_persons_exist = ensure_persons_exist
        self._create_photo_from_obj = create_photo_from_obj
        self._edit_movie_contribution_gateway = edit_movie_contribution_gateway
        self._user_gateway = user_gateway
        self._movie_gateway = movie_gateway
        self._role_gateway = role_gateway
        self._writer_gateway = writer_gateway
        self._crew_member_gateway = crew_member_gateway
        self._object_storage = object_storage
        self._identity_provider = identity_provider
        self._current_timestamp = current_timestamp

    async def process(
        self,
        command: EditMovieCommand,
    ) -> EditMovieContributionId:
        current_user_id = await self._identity_provider.user_id()

        author = await self._user_gateway.with_id(current_user_id)
        if not author:
            raise UserDoesNotExistError(current_user_id)

        movie = await self._movie_gateway.with_id(command.movie_id)
        if not movie:
            raise MovieDoesNotExistError()

        await self._ensure_roles_exist(command.remove_roles)
        await self._ensure_writers_exist(command.remove_writers)
        await self._ensure_crew_exist(command.remove_crew)

        await self._ensure_persons_exist(
            *(role.person_id for role in command.add_roles),
            *(writer.person_id for writer in command.add_writers),
            *(crew_member.person_id for crew_member in command.add_crew),
        )

        add_photos = [
            self._create_photo_from_obj(obj) for obj in command.add_photos
        ]

        contribution = self._edit_movie(
            id=EditMovieContributionId(uuid7()),
            author=author,
            movie=movie,
            eng_title=command.eng_title,
            original_title=command.original_title,
            release_date=command.release_date,
            countries=command.countries,
            genres=command.genres,
            mpaa=command.mpaa,
            duration=command.duration,
            budget=command.budget,
            revenue=command.revenue,
            add_roles=command.add_roles,
            remove_roles=command.remove_roles,
            add_writers=command.add_writers,
            remove_writers=command.remove_writers,
            add_crew=command.add_crew,
            remove_crew=command.remove_crew,
            add_photos=[photo.url for photo in add_photos],
            current_timestamp=self._current_timestamp,
        )
        await self._edit_movie_contribution_gateway.save(contribution)

        await self._object_storage.save_photo_seq(add_photos)

        return contribution.id

    async def _ensure_roles_exist(
        self,
        roles_ids: Sequence[RoleId],
    ) -> None:
        roles_from_gateway = await self._role_gateway.list_with_ids(
            *roles_ids,
        )
        some_of_roles_do_not_exist = len(roles_ids) != len(
            roles_from_gateway,
        )

        if some_of_roles_do_not_exist:
            ids_of_roles_from_gateway = [
                role_from_gateway.id
                for role_from_gateway in roles_from_gateway
            ]
            ids_of_missing_roles = set(roles_ids).difference(
                ids_of_roles_from_gateway,
            )
            raise RolesDoNotExistError(list(ids_of_missing_roles))

    async def _ensure_writers_exist(
        self,
        writers_ids: Sequence[WriterId],
    ) -> None:
        writers_from_gateway = await self._writer_gateway.list_with_ids(
            *writers_ids,
        )
        some_of_writers_do_not_exist = len(writers_ids) != len(
            writers_from_gateway,
        )

        if some_of_writers_do_not_exist:
            ids_of_writers_from_gateway = [
                writer_from_gateway.id
                for writer_from_gateway in writers_from_gateway
            ]
            ids_of_missing_writers = set(writers_ids).difference(
                ids_of_writers_from_gateway,
            )
            raise WritersDoNotExistError(list(ids_of_missing_writers))

    async def _ensure_crew_exist(
        self,
        crew_members_ids: Sequence[CrewMemberId],
    ) -> None:
        crew_members_from_gateway = (
            await self._crew_member_gateway.list_with_ids(
                *crew_members_ids,
            )
        )
        some_of_crew_members_do_not_exist = len(crew_members_ids) != len(
            crew_members_from_gateway,
        )

        if some_of_crew_members_do_not_exist:
            ids_of_crew_members_from_gateway = [
                crew_member_from_gateway.id
                for crew_member_from_gateway in crew_members_from_gateway
            ]
            ids_of_missing_crew_members = set(crew_members_ids).difference(
                ids_of_crew_members_from_gateway,
            )
            raise CrewMembersDoNotExistError(list(ids_of_missing_crew_members))


class CallbackProcessor:
    def __init__(
        self,
        *,
        processor: AuthorizationProcessor,
        create_photo_from_obj: CreatePhotoFromObj,
        identity_provider: IdentityProvider,
        on_movie_edited: OnMovieEdited,
        current_timestamp: datetime,
    ):
        self._processor = processor
        self._create_photo_from_obj = create_photo_from_obj
        self._identity_provider = identity_provider
        self._on_movie_edited = on_movie_edited
        self._current_timestamp = current_timestamp

    async def process(
        self,
        command: EditMovieCommand,
    ) -> EditMovieContributionId:
        result = await self._processor.process(command)
        current_user_id = await self._identity_provider.user_id()
        add_photos = [
            self._create_photo_from_obj(obj) for obj in command.add_photos
        ]

        await self._on_movie_edited(
            id=result,
            author_id=current_user_id,
            movie_id=command.movie_id,
            eng_title=command.eng_title,
            original_title=command.original_title,
            release_date=command.release_date,
            countries=command.countries,
            genres=command.genres,
            mpaa=command.mpaa,
            duration=command.duration,
            budget=command.budget,
            revenue=command.revenue,
            add_roles=command.add_roles,
            remove_roles=command.remove_roles,
            add_writers=command.add_writers,
            remove_writers=command.remove_writers,
            add_crew=command.add_crew,
            remove_crew=command.remove_crew,
            add_photos=[photo.url for photo in add_photos],
            edited_at=self._current_timestamp,
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
        command: EditMovieCommand,
    ) -> EditMovieContributionId:
        current_user_id = await self._identity_provider.user_id()
        command_processing_id = uuid7()

        logger.debug(
            "'Edit Movie' command processing started",
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
        except MovieDoesNotExistError as e:
            logger.error(
                "Unexpected error occurred: Movie doesn't exist",
                extra={"processing_id": command_processing_id},
            )
            raise e
        except UserIsNotActiveError as e:
            logger.debug(
                "Expected error occurred: User is not active",
                extra={"processing_id": command_processing_id},
            )
            raise e
        except RolesDoNotExistError as e:
            logger.debug(
                "Expected error occurred: "
                "Roles ids entered by user do not belong to any roles",
                extra={
                    "processing_id": command_processing_id,
                    "ids_of_missing_roles": e.ids_of_missing_roles,
                },
            )
            raise e
        except WritersDoNotExistError as e:
            logger.debug(
                "Expected error occurred: "
                "Writers ids entered by user do not belong to any writers",
                extra={
                    "processing_id": command_processing_id,
                    "ids_of_missing_writers": e.ids_of_missing_writers,
                },
            )
            raise e
        except CrewMembersDoNotExistError as e:
            logger.debug(
                "Expected error occurred: "
                "Crew members ids entered by user do not belong to any"
                "crew members",
                extra={
                    "processing_id": command_processing_id,
                    "ids_of_missing_crew_members": e.ids_of_missing_crew_members,
                },
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
            "'Edit Movie' command processing completed",
            extra={
                "processing_id": command_processing_id,
                "contribution_id": result,
            },
        )

        return result
