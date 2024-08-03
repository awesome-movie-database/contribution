import logging

from contribution.domain import (
    InvalidMovieEngTitleError,
    InvalidMovieOriginalTitleError,
    InvalidMovieDurationError,
    UpdateMovie,
)
from contribution.application.common import (
    OperationId,
    CreateAndSaveRoles,
    DeleteRoles,
    CreateAndSaveWriters,
    DeleteWriters,
    CreateAndSaveCrew,
    DeleteCrew,
    CommandProcessor,
    TransactionProcessor,
    MovieDoesNotExistError,
    PersonsDoNotExistError,
    RolesAlreadyExistError,
    RolesDoNotExistError,
    WritersAlreadyExistError,
    WritersDoNotExistError,
    CrewMembersAlreadyExistError,
    CrewMembersDoNotExistError,
    MovieGateway,
    PersonGateway,
    UnitOfWork,
)
from contribution.application.commands import UpdateMovieCommand


logger = logging.getLogger(__name__)


def update_movie_factory(
    operation_id: OperationId,
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
    log_processor = UpdateMovieLoggingProcessor(
        processor=tx_processor,
        operation_id=operation_id,
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
        movie = await self._movie_gateway.acquire_by_id(command.movie_id)
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
            contribution_roles=command.add_roles,
        )
        await self._create_and_save_writers(
            movie=movie,
            contribution_writers=command.add_writers,
        )
        await self._create_and_save_crew(
            movie=movie,
            contribution_crew=command.add_crew,
        )

        await self._delete_roles(command.remove_roles)
        await self._delete_writers(command.remove_writers)
        await self._delete_crew(command.remove_crew)


class UpdateMovieLoggingProcessor:
    def __init__(
        self,
        *,
        processor: TransactionProcessor,
        operation_id: OperationId,
    ):
        self._processor = processor
        self._operation_id = operation_id

    async def process(self, command: UpdateMovieCommand) -> None:
        logger.debug(
            "'Update Movie' command processing started",
            extra={
                "operation_id": self._operation_id,
                "command": command,
            },
        )

        try:
            result = await self._processor.process(command)
        except MovieDoesNotExistError as error:
            logger.error(
                "Unexpected error occurred: Movie doesn't exist",
                extra={"operation_id": self._operation_id},
            )
            raise error
        except InvalidMovieEngTitleError as error:
            logger.error(
                "Unexpected error occurred: Invalid movie eng title",
                extra={"operation_id": self._operation_id},
            )
            raise error
        except InvalidMovieOriginalTitleError as error:
            logger.error(
                "Unexpected error occurred: Invalid movie original title",
                extra={"operation_id": self._operation_id},
            )
            raise error
        except InvalidMovieDurationError as error:
            logger.error(
                "Unexpected error occurred: Invalid movie duration",
                extra={"operation_id": self._operation_id},
            )
            raise error
        except PersonsDoNotExistError as error:
            logger.error(
                "Unexpected error occurred: "
                "Person ids do not belong to any persons",
                extra={
                    "operation_id": self._operation_id,
                    "ids_of_missing_persons": error.ids_of_missing_persons,
                },
            )
            raise error
        except RolesAlreadyExistError as error:
            logger.error(
                "Unexpected error occurred: "
                "Role ids already belong to some roles",
                extra={
                    "operation_id": self._operation_id,
                    "ids_of_existing_roles": error.ids_of_existing_roles,
                },
            )
            raise error
        except RolesDoNotExistError as error:
            logger.error(
                "Unexpected error occurred: "
                "Role ids do not belong to any roles",
                extra={
                    "operation_id": self._operation_id,
                    "ids_of_missing_roles": error.ids_of_missing_roles,
                },
            )
            raise error
        except WritersAlreadyExistError as error:
            logger.error(
                "Unexpected error occurred: "
                "Writer ids already belong to some writers",
                extra={
                    "operation_id": self._operation_id,
                    "ids_of_existing_writers": error.ids_of_existing_writers,
                },
            )
            raise error
        except WritersDoNotExistError as error:
            logger.error(
                "Unexpected error occurred: "
                "Writer ids do not belong to any writers",
                extra={
                    "operation_id": self._operation_id,
                    "ids_of_missing_writers": error.ids_of_missing_writers,
                },
            )
            raise error
        except CrewMembersAlreadyExistError as error:
            logger.error(
                "Unexpected error occurred: "
                "Crew member ids already belong to some crew members",
                extra={
                    "operation_id": self._operation_id,
                    "ids_of_existing_crew_members": error.ids_of_existing_crew_members,
                },
            )
            raise error
        except CrewMembersDoNotExistError as error:
            logger.error(
                "Unexpected error occurred: "
                "Crew member ids do not belong to any crew members",
                extra={
                    "operation_id": self._operation_id,
                    "ids_of_missing_crew_members": error.ids_of_missing_crew_members,
                },
            )
            raise error
        except Exception as error:
            logger.exception(
                "Unexpected error occurred",
                extra={"operation_id": self._operation_id},
            )
            raise error

        logger.debug(
            "'Update Movie' command processing completed",
            extra={"operation_id": self._operation_id},
        )

        return result
