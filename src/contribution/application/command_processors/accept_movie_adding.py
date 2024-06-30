import logging
from typing import Optional

from uuid_extensions import uuid7

from contribution.domain import (
    AchievementId,
    InvalidMovieEngTitleError,
    InvalidMovieOriginalTitleError,
    InvalidMovieDurationError,
    AcceptContribution,
    CreateMovie,
)
from contribution.application.common import (
    OperationId,
    CreateAndSaveRoles,
    CreateAndSaveWriters,
    CreateAndSaveCrew,
    CommandProcessor,
    TransactionProcessor,
    AchievementEearnedCallbackProcessor,
    MovieIdIsAlreadyTakenError,
    UserDoesNotExistError,
    ContributionDoesNotExistError,
    RolesAlreadyExistError,
    WritersAlreadyExistError,
    CrewMembersAlreadyExistError,
    PersonsDoNotExistError,
    AchievementDoesNotExistError,
    AddMovieContributionGateway,
    MovieGateway,
    UserGateway,
    AchievementGateway,
    UnitOfWork,
    OnEventOccurred,
    AchievementEarnedEvent,
)
from contribution.application.commands import AcceptMovieAddingCommand


logger = logging.getLogger(__name__)


def accept_movie_adding_factory(
    operation_id: OperationId,
    accept_contribution: AcceptContribution,
    create_movie: CreateMovie,
    create_and_save_roles: CreateAndSaveRoles,
    create_and_save_writers: CreateAndSaveWriters,
    create_and_save_crew: CreateAndSaveCrew,
    add_movie_contribution_gateway: AddMovieContributionGateway,
    user_gateway: UserGateway,
    movie_gateway: MovieGateway,
    achievement_gateway: AchievementGateway,
    unit_of_work: UnitOfWork,
    on_achievement_earned: OnEventOccurred[AchievementEarnedEvent],
) -> CommandProcessor[AcceptMovieAddingCommand, Optional[AchievementId]]:
    accept_movie_addition_processor = AcceptMovieAddingProcessor(
        accept_contribution=accept_contribution,
        create_movie=create_movie,
        create_and_save_roles=create_and_save_roles,
        create_and_save_writers=create_and_save_writers,
        create_and_save_crew=create_and_save_crew,
        add_movie_contribution_gateway=add_movie_contribution_gateway,
        user_gateway=user_gateway,
        movie_gateway=movie_gateway,
        achievement_gateway=achievement_gateway,
    )
    callback_processor = AchievementEearnedCallbackProcessor(
        processor=accept_movie_addition_processor,
        achievement_gateway=achievement_gateway,
        on_achievement_earned=on_achievement_earned,
    )
    tx_processor = TransactionProcessor(
        processor=callback_processor,
        unit_of_work=unit_of_work,
    )
    log_processor = AcceptMovieAddingLoggingProcessor(
        processor=tx_processor,
        operation_id=operation_id,
    )

    return log_processor


class AcceptMovieAddingProcessor:
    def __init__(
        self,
        *,
        accept_contribution: AcceptContribution,
        create_movie: CreateMovie,
        create_and_save_roles: CreateAndSaveRoles,
        create_and_save_writers: CreateAndSaveWriters,
        create_and_save_crew: CreateAndSaveCrew,
        add_movie_contribution_gateway: AddMovieContributionGateway,
        user_gateway: UserGateway,
        movie_gateway: MovieGateway,
        achievement_gateway: AchievementGateway,
    ):
        self._accept_contribution = accept_contribution
        self._create_movie = create_movie
        self._create_and_save_roles = create_and_save_roles
        self._create_and_save_writers = create_and_save_writers
        self._create_and_save_crew = create_and_save_crew
        self._add_movie_contribution_gateway = add_movie_contribution_gateway
        self._user_gateway = user_gateway
        self._movie_gateway = movie_gateway
        self._achievement_gateway = achievement_gateway

    async def process(
        self,
        command: AcceptMovieAddingCommand,
    ) -> Optional[AchievementId]:
        contribution = (
            await self._add_movie_contribution_gateway.acquire_by_id(
                id=command.contribution_id,
            )
        )
        if not contribution:
            raise ContributionDoesNotExistError()

        author = await self._user_gateway.acquire_by_id(
            id=contribution.author_id,
        )
        if not author:
            raise UserDoesNotExistError()

        movie = await self._movie_gateway.by_id(command.movie_id)
        if movie:
            raise MovieIdIsAlreadyTakenError()

        achievement = self._accept_contribution(
            achievement_id=AchievementId(uuid7()),
            contribution=contribution,
            author=author,
            current_timestamp=command.accepted_at,
        )
        if achievement:
            await self._achievement_gateway.save(achievement)

        await self._user_gateway.update(author)
        await self._add_movie_contribution_gateway.update(contribution)

        new_movie = self._create_movie(
            id=command.movie_id,
            eng_title=contribution.eng_title,
            original_title=contribution.original_title,
            release_date=contribution.release_date,
            countries=contribution.countries,
            genres=contribution.genres,
            mpaa=contribution.mpaa,
            duration=contribution.duration,
            budget=contribution.budget,
            revenue=contribution.revenue,
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

        return achievement.id if achievement else None


class AcceptMovieAddingLoggingProcessor:
    def __init__(
        self,
        *,
        processor: TransactionProcessor,
        operation_id: OperationId,
    ):
        self._processor = processor
        self._operation_id = operation_id

    async def process(
        self,
        command: AcceptMovieAddingCommand,
    ) -> Optional[AchievementId]:
        logger.debug(
            "'Accept Movie Adding' command processing started",
            extra={
                "operation_id": self._operation_id,
                "command": command,
            },
        )

        try:
            result = await self._processor.process(command)
        except ContributionDoesNotExistError as e:
            logger.error(
                "Unexpected error occurred: Contribution doesn't exist",
                extra={"operation_id": self._operation_id},
            )
            raise e
        except UserDoesNotExistError as e:
            logger.error(
                "Unexpected error occurred: Contribution has author id, "
                "using which user gateway returns None",
                extra={"operation_id": self._operation_id},
            )
            raise e
        except MovieIdIsAlreadyTakenError as e:
            logger.error(
                "Unexpected error occurred: Movie id is already taken",
                extra={"operation_id": self._operation_id},
            )
            raise e
        except InvalidMovieEngTitleError as e:
            logger.error(
                "Unexpected error occurred: Invalid movie eng title",
                extra={"operation_id": self._operation_id},
            )
            raise e
        except InvalidMovieOriginalTitleError as e:
            logger.error(
                "Unexpected error occurred: Invalid movie original title",
                extra={"operation_id": self._operation_id},
            )
            raise e
        except InvalidMovieDurationError as e:
            logger.error(
                "Unexpected error occurred: Invalid movie duration",
                extra={"operation_id": self._operation_id},
            )
            raise e
        except RolesAlreadyExistError as e:
            logger.error(
                "Unexpected error occurred: "
                "Role ids already belong to some roles",
                extra={
                    "operation_id": self._operation_id,
                    "ids_of_existing_roles": e.ids_of_existing_roles,
                },
            )
            raise e
        except WritersAlreadyExistError as e:
            logger.error(
                "Unexpected error occurred: "
                "Writer ids already belong to some writers",
                extra={
                    "operation_id": self._operation_id,
                    "ids_of_existing_writers": e.ids_of_existing_writers,
                },
            )
            raise e
        except CrewMembersAlreadyExistError as e:
            logger.error(
                "Unexpected error occurred: "
                "Crew member ids already belong to some crew members",
                extra={
                    "operation_id": self._operation_id,
                    "ids_of_existing_crew_members": (
                        e.ids_of_existing_crew_members,
                    ),
                },
            )
            raise e
        except PersonsDoNotExistError as e:
            logger.error(
                "Unexpected error occurred: "
                "Person ids referenced in contribution roles, writers or crew"
                "are do not belong to any persons",
                extra={
                    "operation_id": self._operation_id,
                    "ids_of_missing_persons": e.ids_of_missing_persons,
                },
            )
            raise e
        except AchievementDoesNotExistError as e:
            logger.error(
                "Unexpected error occurred: Achievement was created, "
                "but achievement gateway returns None",
                extra={"operation_id": self._operation_id},
            )
        except Exception as e:
            logger.exception(
                "Unexpected error occurred",
                exc_info=e,
                extra={
                    "operation_id": self._operation_id,
                    "error": e,
                },
            )
            raise e

        logger.debug(
            "'Accept Movie Adding' command processing completed",
            extra={
                "operation_id": self._operation_id,
                "achievement_id": result,
            },
        )

        return result
