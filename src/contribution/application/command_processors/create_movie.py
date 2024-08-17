import logging

from contribution.domain import (
    InvalidMovieEngTitleError,
    InvalidMovieOriginalTitleError,
    InvalidMovieSummaryError,
    InvalidMovieDescriptionError,
    InvalidMovieDurationError,
    CreateMovie,
)
from contribution.application.common import (
    OperationId,
    CreateAndSaveRoles,
    CreateAndSaveWriters,
    CreateAndSaveCrew,
    CommandProcessor,
    TransactionProcessor,
    MovieIdIsAlreadyTakenError,
    PersonsDoNotExistError,
    RolesAlreadyExistError,
    WritersAlreadyExistError,
    CrewMembersAlreadyExistError,
    MovieGateway,
    PersonGateway,
    UnitOfWork,
)
from contribution.application.commands import CreateMovieCommand


logger = logging.getLogger(__name__)


def create_movie_factory(
    operation_id: OperationId,
    create_movie: CreateMovie,
    create_and_save_roles: CreateAndSaveRoles,
    create_and_save_writers: CreateAndSaveWriters,
    create_and_save_crew: CreateAndSaveCrew,
    movie_gateway: MovieGateway,
    person_gateway: PersonGateway,
    unit_of_work: UnitOfWork,
) -> CommandProcessor[CreateMovieCommand, None]:
    create_movie_processor = CreateMovieProcessor(
        create_movie=create_movie,
        create_and_save_roles=create_and_save_roles,
        create_and_save_writers=create_and_save_writers,
        create_and_save_crew=create_and_save_crew,
        movie_gateway=movie_gateway,
        person_gateway=person_gateway,
    )
    tx_processor = TransactionProcessor(
        processor=create_movie_processor,
        unit_of_work=unit_of_work,
    )
    log_processor = CreateMovieLoggingProcessor(
        processor=tx_processor,
        operation_id=operation_id,
    )

    return log_processor


class CreateMovieProcessor:
    def __init__(
        self,
        *,
        create_movie: CreateMovie,
        create_and_save_roles: CreateAndSaveRoles,
        create_and_save_writers: CreateAndSaveWriters,
        create_and_save_crew: CreateAndSaveCrew,
        movie_gateway: MovieGateway,
        person_gateway: PersonGateway,
    ):
        self._create_movie = create_movie
        self._create_and_save_roles = create_and_save_roles
        self._create_and_save_writers = create_and_save_writers
        self._create_and_save_crew = create_and_save_crew
        self._movie_gateway = movie_gateway
        self._person_gateway = person_gateway

    async def process(self, command: CreateMovieCommand) -> None:
        movie = await self._movie_gateway.by_id(command.id)
        if movie:
            raise MovieIdIsAlreadyTakenError()

        new_movie = self._create_movie(
            id=command.id,
            eng_title=command.eng_title,
            original_title=command.original_title,
            summary=command.summary,
            description=command.description,
            release_date=command.release_date,
            countries=command.countries,
            genres=command.genres,
            mpaa=command.mpaa,
            duration=command.duration,
            budget=command.budget,
            revenue=command.revenue,
        )
        await self._movie_gateway.save(new_movie)

        await self._create_and_save_roles(
            movie=new_movie,
            movie_roles=command.roles,
        )
        await self._create_and_save_writers(
            movie=new_movie,
            movie_writers=command.writers,
        )
        await self._create_and_save_crew(
            movie=new_movie,
            movie_crew=command.crew,
        )


class CreateMovieLoggingProcessor:
    def __init__(
        self,
        *,
        processor: TransactionProcessor,
        operation_id: OperationId,
    ):
        self._processor = processor
        self._operation_id = operation_id

    async def process(self, command: CreateMovieCommand) -> None:
        logger.debug(
            "'Create Movie' command processing started",
            extra={
                "operation_id": self._operation_id,
                "command": command,
            },
        )

        try:
            result = await self._processor.process(command)
        except MovieIdIsAlreadyTakenError as error:
            logger.error(
                "Unexpected error occurred: Movie id is already taken",
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
        except InvalidMovieSummaryError as error:
            logger.error(
                "Unexpected error occurred: Invalid movie summary",
                extra={"operation_id": self._operation_id},
            )
            raise error
        except InvalidMovieDescriptionError as error:
            logger.error(
                "Unexpected error occurred: Invalid movie description",
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
                    "non_existing_persons": error.person_ids,
                },
            )
            raise error
        except RolesAlreadyExistError as error:
            logger.error(
                "Unexpected error occurred: "
                "Role ids already belong to some roles",
                extra={
                    "operation_id": self._operation_id,
                    "existing_role_ids": error.role_ids,
                },
            )
            raise error
        except WritersAlreadyExistError as error:
            logger.error(
                "Unexpected error occurred: "
                "Writer ids already belong to some writers",
                extra={
                    "operation_id": self._operation_id,
                    "existing_writer_ids": error.writer_ids,
                },
            )
            raise error
        except CrewMembersAlreadyExistError as error:
            logger.error(
                "Unexpected error occurred: "
                "Crew member ids already belong to some crew members",
                extra={
                    "operation_id": self._operation_id,
                    "existing_crew_member_ids": error.crew_member_ids,
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
            "'Create Movie' command processing completed",
            extra={"operation_id": self._operation_id},
        )

        return result
