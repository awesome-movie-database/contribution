import logging
from typing import Sequence

from uuid_extensions import uuid7

from contribution.domain.entities import (
    Movie,
    Role,
    Writer,
    CrewMember,
)
from contribution.domain.exceptions import (
    InvalidMovieEngTitleError,
    InvalidMovieOriginalTitleError,
    InvalidMovieDurationError,
)
from contribution.domain.services import (
    CreateMovie,
    CreateRole,
    CreateWriter,
    CreateCrewMember,
)
from contribution.application.common.value_objects import (
    MovieRole,
    MovieWriter,
    MovieCrewMember,
)
from contribution.application.common.services import (
    EnsurePersonsExist,
    EnsureRolesDoNotExist,
    EnsureWritersDoNotExist,
    EnsureCrewMembersDoNotExist,
)
from contribution.application.common.command_processors import (
    CommandProcessor,
    TransactionProcessor,
)
from contribution.application.common.exceptions import (
    MovieIdIsAlreadyTakenError,
    PersonsDoNotExistError,
    RolesAlreadyExistError,
    WritersAlreadyExistError,
    CrewMembersAlreadyExistError,
)
from contribution.application.common.gateways import (
    MovieGateway,
    PersonGateway,
    RoleGateway,
    WriterGateway,
    CrewMemberGateway,
)
from contribution.application.common.unit_of_work import UnitOfWork
from contribution.application.commands import CreateMovieCommand


logger = logging.getLogger(__name__)


def create_movie_factory(
    create_movie: CreateMovie,
    create_role: CreateRole,
    create_writer: CreateWriter,
    create_crew_member: CreateCrewMember,
    ensure_persons_exist: EnsurePersonsExist,
    ensure_roles_do_not_exist: EnsureRolesDoNotExist,
    ensure_writers_do_not_exist: EnsureWritersDoNotExist,
    ensure_crew_members_do_not_exist: EnsureCrewMembersDoNotExist,
    movie_gateway: MovieGateway,
    person_gateway: PersonGateway,
    role_gateway: RoleGateway,
    writer_gateway: WriterGateway,
    crew_member_gateway: CrewMemberGateway,
    unit_of_work: UnitOfWork,
) -> CommandProcessor[CreateMovieCommand, None]:
    create_movie_processor = CreateMovieProcessor(
        create_movie=create_movie,
        create_role=create_role,
        create_writer=create_writer,
        create_crew_member=create_crew_member,
        ensure_persons_exist=ensure_persons_exist,
        ensure_roles_do_not_exist=ensure_roles_do_not_exist,
        ensure_writers_do_not_exist=ensure_writers_do_not_exist,
        ensure_crew_members_do_not_exist=ensure_crew_members_do_not_exist,
        movie_gateway=movie_gateway,
        person_gateway=person_gateway,
        role_gateway=role_gateway,
        writer_gateway=writer_gateway,
        crew_member_gateway=crew_member_gateway,
    )
    tx_processor = TransactionProcessor(
        processor=create_movie_processor,
        unit_of_work=unit_of_work,
    )
    log_processor = LoggingProcessor(
        processor=tx_processor,
    )

    return log_processor


class CreateMovieProcessor:
    def __init__(
        self,
        *,
        create_movie: CreateMovie,
        create_role: CreateRole,
        create_writer: CreateWriter,
        create_crew_member: CreateCrewMember,
        ensure_persons_exist: EnsurePersonsExist,
        ensure_roles_do_not_exist: EnsureRolesDoNotExist,
        ensure_writers_do_not_exist: EnsureWritersDoNotExist,
        ensure_crew_members_do_not_exist: EnsureCrewMembersDoNotExist,
        movie_gateway: MovieGateway,
        person_gateway: PersonGateway,
        role_gateway: RoleGateway,
        writer_gateway: WriterGateway,
        crew_member_gateway: CrewMemberGateway,
    ):
        self._create_movie = create_movie
        self._create_role = create_role
        self._create_writer = create_writer
        self._create_crew_member = create_crew_member
        self._ensure_persons_exist = ensure_persons_exist
        self._ensure_roles_do_not_exist = ensure_roles_do_not_exist
        self._ensure_writers_do_not_exist = ensure_writers_do_not_exist
        self._ensure_crew_members_do_not_exist = ensure_crew_members_do_not_exist
        self._movie_gateway = movie_gateway
        self._person_gateway = person_gateway
        self._role_gateway = role_gateway
        self._writer_gateway = writer_gateway
        self._crew_member_gateway = crew_member_gateway

    async def process(self, command: CreateMovieCommand) -> None:
        movie = await self._movie_gateway.with_id(command.id)
        if not movie:
            raise MovieIdIsAlreadyTakenError()

        new_movie = self._create_movie(
            id=command.id,
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
        await self._movie_gateway.save(new_movie)

        await self._ensure_persons_exist(
            *(role.person_id for role in command.roles),
            *(writer.person_id for writer in command.writers),
            *(crew_member.person_id for crew_member in command.crew),
        )

        await self._ensure_roles_do_not_exist(
            *(role.id for role in command.roles)
        )
        await self._ensure_writers_do_not_exist(
            *(writer.id for writer in command.writers)
        )
        await self._ensure_crew_members_do_not_exist(
            *(crew_member.id for crew_member in command.crew)
        )

        roles = await self._create_roles(
            movie=movie,
            movie_roles=command.roles,
        )
        await self._role_gateway.save_seq(roles)

        writers = await self._create_writers(
            movie=movie,
            movie_writers=command.writers,
        )
        await self._writer_gateway.save_seq(writers)

        crew_members = await self._create_crew_members(
            movie=movie,
            movie_crew_members=command.crew,
        )
        await self._crew_member_gateway.save_seq(crew_members)

    async def _create_roles(
        self,
        *,
        movie: Movie,
        movie_roles: Sequence[MovieRole],
    ) -> list[Role]:
        persons = await self._person_gateway.list_with_ids(
            *(movie_role.person_id for movie_role in movie_roles),
        )

        roles = []
        for movie_role, person in zip(movie_roles, persons):
            role = self._create_role(
                id=movie_role.id,
                movie=movie,
                person=person,
                character=movie_role.character,
                importance=movie_role.importance,
                is_spoiler=movie_role.is_spoiler,
            )
            roles.append(role)

        return roles

    async def _create_writers(
        self,
        *,
        movie: Movie,
        movie_writers: Sequence[MovieWriter],
    ) -> list[Writer]:
        persons = await self._person_gateway.list_with_ids(
            *(
                movie_writer.person_id
                for movie_writer in movie_writers
            ),
        )

        writers = []
        for movie_writer, person in zip(movie_writers, persons):
            writer = self._create_writer(
                id=movie_writer.id,
                movie=movie,
                person=person,
                writing=movie_writer.writing,
            )
            writers.append(writer)

        return writers

    async def _create_crew_members(
        self,
        *,
        movie: Movie,
        movie_crew_members: Sequence[MovieCrewMember],
    ) -> list[CrewMember]:
        persons = await self._person_gateway.list_with_ids(
            *(
                movie_crew_member.person_id
                for movie_crew_member in movie_crew_members
            ),
        )

        crew_members = []
        for movie_crew_member, person in zip(
            movie_crew_members,
            persons,
        ):
            crew_member = self._create_crew_member(
                id=movie_crew_member.id,
                movie=movie,
                person=person,
                membership=movie_crew_member.membership,
            )
            crew_members.append(crew_member)

        return crew_members


class LoggingProcessor:
    def __init__(self, processor: TransactionProcessor):
        self._processor = processor

    async def process(self, command: CreateMovieCommand) -> None:
        command_processing_id = uuid7()

        logger.debug(
            "'Create Movie' command processing started",
            extra={
                "processing_id": command_processing_id,
                "command": command,
            },
        )

        try:
            result = await self._processor.process(command)
        except MovieIdIsAlreadyTakenError as e:
            logger.error(
                "Unexpected error occurred: Movie id is already taken",
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
            "'Create Movie' command processing completed",
            extra={"processing_id": command_processing_id},
        )

        return result
