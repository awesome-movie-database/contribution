import logging
from typing import Sequence

from uuid_extensions import uuid7

from contribution.domain.value_objects import (
    RoleId,
    WriterId,
    CrewMemberId,
)
from contribution.domain.exceptions import (
    InvalidMovieEngTitleError,
    InvalidMovieOriginalTitleError,
    InvalidMovieDurationError,
)
from contribution.domain.services import UpdateMovie
from contribution.application.common.services import (
    CreateRoles,
    CreateWriters,
    CreateCrew,
)
from contribution.application.common.command_processors import (
    CommandProcessor,
    TransactionProcessor,
)
from contribution.application.common.exceptions import (
    MovieDoesNotExistError,
    PersonsDoNotExistError,
    RolesAlreadyExistError,
    RolesDoNotExistError,
    WritersAlreadyExistError,
    WritersDoNotExistError,
    CrewMembersAlreadyExistError,
    CrewMembersDoNotExistError,
)
from contribution.application.common.gateways import (
    MovieGateway,
    PersonGateway,
    RoleGateway,
    WriterGateway,
    CrewMemberGateway,
)
from contribution.application.common.unit_of_work import UnitOfWork
from contribution.application.commands import UpdateMovieCommand


logger = logging.getLogger(__name__)


def update_movie_factory(
    update_movie: UpdateMovie,
    create_roles: CreateRoles,
    create_writers: CreateWriters,
    create_crew: CreateCrew,
    movie_gateway: MovieGateway,
    person_gateway: PersonGateway,
    role_gateway: RoleGateway,
    writer_gateway: WriterGateway,
    crew_member_gateway: CrewMemberGateway,
    unit_of_work: UnitOfWork,
) -> CommandProcessor[UpdateMovieCommand, None]:
    update_movie_processor = UpdateMovieProcessor(
        update_movie=update_movie,
        create_roles=create_roles,
        create_writers=create_writers,
        create_crew=create_crew,
        movie_gateway=movie_gateway,
        person_gateway=person_gateway,
        role_gateway=role_gateway,
        writer_gateway=writer_gateway,
        crew_member_gateway=crew_member_gateway,
    )
    tx_processor = TransactionProcessor(
        processor=update_movie_processor,
        unit_of_work=unit_of_work,
    )
    log_processor = LoggingProcessor(
        processor=tx_processor,
    )

    return log_processor


class UpdateMovieProcessor:
    def __init__(
        self,
        *,
        update_movie: UpdateMovie,
        create_roles: CreateRoles,
        create_writers: CreateWriters,
        create_crew: CreateCrew,
        movie_gateway: MovieGateway,
        person_gateway: PersonGateway,
        role_gateway: RoleGateway,
        writer_gateway: WriterGateway,
        crew_member_gateway: CrewMemberGateway,
    ):
        self._update_movie = update_movie
        self._create_roles = create_roles
        self._create_writers = create_writers
        self._create_crew = create_crew
        self._movie_gateway = movie_gateway
        self._person_gateway = person_gateway
        self._role_gateway = role_gateway
        self._writer_gateway = writer_gateway
        self._crew_member_gateway = crew_member_gateway

    async def process(self, command: UpdateMovieCommand) -> None:
        movie = await self._movie_gateway.acquire_with_id(command.movie_id)
        if not movie:
            raise MovieDoesNotExistError()

        self._update_movie(
            movie,
            eng_title=command.eng_title,
            original_title=command.original_title,
            release_date=command.release_date,
            countries=command.countries,
            genres=command.genres,
            mpaa=command.mpaa,
            duration=command.duration,
            budget=command.budget,
            revenue=command.revenue,
        )
        await self._movie_gateway.update(movie)

        roles_for_saving = await self._create_roles(
            movie=movie,
            movie_roles=command.add_roles,
        )
        await self._role_gateway.save_seq(roles_for_saving)

        writers_for_saving = await self._create_writers(
            movie=movie,
            movie_writers=command.add_writers,
        )
        await self._writer_gateway.save_seq(writers_for_saving)

        crew_for_saving = await self._create_crew(
            movie=movie,
            movie_crew=command.add_crew,
        )
        await self._crew_member_gateway.save_seq(crew_for_saving)

        await self._ensure_roles_exist(command.remove_roles)
        await self._ensure_writers_exist(command.remove_writers)
        await self._ensure_crew_exist(command.remove_crew)

        roles = await self._role_gateway.list_with_ids(
            *command.remove_roles,
        )
        await self._role_gateway.delete_seq(roles)

        writers = await self._writer_gateway.list_with_ids(
            *command.remove_writers,
        )
        await self._writer_gateway.delete_seq(writers)

        crew_members = await self._crew_member_gateway.list_with_ids(
            *command.remove_crew,
        )
        await self._crew_member_gateway.delete_seq(crew_members)

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


class LoggingProcessor:
    def __init__(self, processor: TransactionProcessor):
        self._processor = processor

    async def process(self, command: UpdateMovieCommand) -> None:
        command_processing_id = uuid7()

        logger.debug(
            "'Update Movie' command processing started",
            extra={
                "processing_id": command_processing_id,
                "command": command,
            },
        )

        try:
            result = await self._processor.process(command)
        except MovieDoesNotExistError as e:
            logger.error(
                "Unexpected error occurred: Movie id doesn't exist",
                extra={"processing_id": command_processing_id},
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
        except PersonsDoNotExistError as e:
            logger.error(
                "Unexpected error occurred: "
                "Person ids do not belong to any persons",
                extra={
                    "processing_id": command_processing_id,
                    "ids_of_missing_persons": e.ids_of_missing_persons,
                },
            )
            raise e
        except RolesAlreadyExistError as e:
            logger.error(
                "Unexpected error occurred: "
                "Role ids already belong to some roles",
                extra={
                    "processing_id": command_processing_id,
                    "ids_of_existing_roles": e.ids_of_existing_roles,
                },
            )
            raise e
        except RolesDoNotExistError as e:
            logger.error(
                "Unexpected error occurred: "
                "Role ids do not belong to any roles",
                extra={
                    "processing_id": command_processing_id,
                    "ids_of_missing_roles": e.ids_of_missing_roles,
                },
            )
            raise e
        except WritersAlreadyExistError as e:
            logger.error(
                "Unexpected error occurred: "
                "Writer ids already belong to some writers",
                extra={
                    "processing_id": command_processing_id,
                    "ids_of_existing_writers": e.ids_of_existing_writers,
                },
            )
            raise e
        except WritersDoNotExistError as e:
            logger.error(
                "Unexpected error occurred: "
                "Writer ids do not belong to any writers",
                extra={
                    "processing_id": command_processing_id,
                    "ids_of_missing_writers": e.ids_of_missing_writers,
                },
            )
            raise e
        except CrewMembersAlreadyExistError as e:
            logger.error(
                "Unexpected error occurred: "
                "Crew member ids already belong to some crew members",
                extra={
                    "processing_id": command_processing_id,
                    "ids_of_existing_crew_members": e.ids_of_existing_crew_members,
                },
            )
            raise e
        except CrewMembersDoNotExistError as e:
            logger.error(
                "Unexpected error occurred: "
                "Crew member ids do not belong to any crew members",
                extra={
                    "processing_id": command_processing_id,
                    "ids_of_missing_crew_members": e.ids_of_missing_crew_members,
                },
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
            "'Update Movie' command processing completed",
            extra={"processing_id": command_processing_id},
        )

        return result
