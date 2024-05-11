import logging

from uuid_extensions import uuid7

from contribution.domain.exceptions import (
    InvalidMovieEngTitleError,
    InvalidMovieOriginalTitleError,
    InvalidMovieDurationError,
)
from contribution.domain.services import UpdateMovie
from contribution.application.common.services import (
    CreateAndSaveRoles,
    DeleteRoles,
    CreateAndSaveWriters,
    DeleteWriters,
    CreateAndSaveCrew,
    DeleteCrew,
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
)
from contribution.application.common.unit_of_work import UnitOfWork
from contribution.application.commands import UpdateMovieCommand


logger = logging.getLogger(__name__)


def update_movie_factory(
    update_movie: UpdateMovie,
    create_and_save_roles: CreateAndSaveRoles,
    delete_roles: DeleteRoles,
    create_and_save_writers: CreateAndSaveWriters,
    delete_writers: DeleteWriters,
    create_and_save_crew: CreateAndSaveCrew,
    delete_crew: DeleteCrew,
    movie_gateway: MovieGateway,
    person_gateway: PersonGateway,
    unit_of_work: UnitOfWork,
) -> CommandProcessor[UpdateMovieCommand, None]:
    update_movie_processor = UpdateMovieProcessor(
        update_movie=update_movie,
        create_and_save_roles=create_and_save_roles,
        delete_roles=delete_roles,
        create_and_save_writers=create_and_save_writers,
        delete_writers=delete_writers,
        create_and_save_crew=create_and_save_crew,
        delete_crew=delete_crew,
        movie_gateway=movie_gateway,
        person_gateway=person_gateway,
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
        create_and_save_roles: CreateAndSaveRoles,
        delete_roles: DeleteRoles,
        create_and_save_writers: CreateAndSaveWriters,
        delete_writers: DeleteWriters,
        create_and_save_crew: CreateAndSaveCrew,
        delete_crew: DeleteCrew,
        movie_gateway: MovieGateway,
        person_gateway: PersonGateway,
    ):
        self._update_movie = update_movie
        self._create_and_save_roles = create_and_save_roles
        self._delete_roles = delete_roles
        self._create_and_save_writers = create_and_save_writers
        self._delete_writers = delete_writers
        self._create_and_save_crew = create_and_save_crew
        self._delete_crew = delete_crew
        self._movie_gateway = movie_gateway
        self._person_gateway = person_gateway

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

        await self._create_and_save_roles(
            movie=movie,
            movie_roles=command.add_roles,
        )
        await self._create_and_save_writers(
            movie=movie,
            movie_writers=command.add_writers,
        )
        await self._create_and_save_crew(
            movie=movie,
            movie_crew=command.add_crew,
        )

        await self._delete_roles(command.remove_roles)
        await self._delete_writers(command.remove_writers)
        await self._delete_crew(command.remove_crew)


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
                "Unexpected error occurred: Movie doesn't exist",
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
