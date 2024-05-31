import logging
from typing import Optional

from uuid_extensions import uuid7

from contribution.domain import (
    AchievementId,
    InvalidMovieEngTitleError,
    InvalidMovieOriginalTitleError,
    InvalidMovieDurationError,
    AcceptContribution,
    UpdateMovie,
)
from contribution.application.common import (
    CorrelationId,
    CreateAndSaveRoles,
    DeleteRoles,
    CreateAndSaveWriters,
    DeleteWriters,
    CreateAndSaveCrew,
    DeleteCrew,
    CommandProcessor,
    TransactionProcessor,
    AchievementEearnedCallbackProcessor,
    MovieDoesNotExistError,
    UserDoesNotExistError,
    ContributionDoesNotExistError,
    RolesAlreadyExistError,
    RolesDoNotExistError,
    WritersAlreadyExistError,
    WritersDoNotExistError,
    CrewMembersAlreadyExistError,
    CrewMembersDoNotExistError,
    PersonsDoNotExistError,
    AchievementDoesNotExistError,
    EditMovieContributionGateway,
    MovieGateway,
    UserGateway,
    AchievementGateway,
    UnitOfWork,
    OnEventOccurred,
    AchievementEarnedEvent,
)
from contribution.application.commands import AcceptMovieEditingCommand


logger = logging.getLogger(__name__)


def accept_movie_editing_factory(
    correlation_id: CorrelationId,
    accept_contribution: AcceptContribution,
    update_movie: UpdateMovie,
    create_and_save_roles: CreateAndSaveRoles,
    delete_roles: DeleteRoles,
    create_and_save_writers: CreateAndSaveWriters,
    delete_writers: DeleteWriters,
    create_and_save_crew: CreateAndSaveCrew,
    delete_crew: DeleteCrew,
    edit_movie_contribution_gateway: EditMovieContributionGateway,
    user_gateway: UserGateway,
    movie_gateway: MovieGateway,
    achievement_gateway: AchievementGateway,
    unit_of_work: UnitOfWork,
    on_achievement_earned: OnEventOccurred[AchievementEarnedEvent],
) -> CommandProcessor[AcceptMovieEditingCommand, Optional[AchievementId]]:
    accept_movie_editing_processor = AcceptMovieEditingProcessor(
        accept_contribution=accept_contribution,
        update_movie=update_movie,
        create_and_save_roles=create_and_save_roles,
        delete_roles=delete_roles,
        create_and_save_writers=create_and_save_writers,
        delete_writers=delete_writers,
        create_and_save_crew=create_and_save_crew,
        delete_crew=delete_crew,
        edit_movie_contribution_gateway=edit_movie_contribution_gateway,
        user_gateway=user_gateway,
        movie_gateway=movie_gateway,
        achievement_gateway=achievement_gateway,
    )
    callback_processor = AchievementEearnedCallbackProcessor(
        processor=accept_movie_editing_processor,
        achievement_gateway=achievement_gateway,
        on_achievement_earned=on_achievement_earned,
    )
    tx_processor = TransactionProcessor(
        processor=callback_processor,
        unit_of_work=unit_of_work,
    )
    log_processor = LoggingProcessor(
        processor=tx_processor,
        correlation_id=correlation_id,
    )

    return log_processor


class AcceptMovieEditingProcessor:
    def __init__(
        self,
        *,
        accept_contribution: AcceptContribution,
        update_movie: UpdateMovie,
        create_and_save_roles: CreateAndSaveRoles,
        delete_roles: DeleteRoles,
        create_and_save_writers: CreateAndSaveWriters,
        delete_writers: DeleteWriters,
        create_and_save_crew: CreateAndSaveCrew,
        delete_crew: DeleteCrew,
        edit_movie_contribution_gateway: EditMovieContributionGateway,
        user_gateway: UserGateway,
        movie_gateway: MovieGateway,
        achievement_gateway: AchievementGateway,
    ):
        self._accept_contribution = accept_contribution
        self._update_movie = update_movie
        self._create_and_save_roles = create_and_save_roles
        self._delete_roles = delete_roles
        self._create_and_save_writers = create_and_save_writers
        self._delete_writers = delete_writers
        self._create_and_save_crew = create_and_save_crew
        self._delete_crew = delete_crew
        self._edit_movie_contribution_gateway = edit_movie_contribution_gateway
        self._user_gateway = user_gateway
        self._movie_gateway = movie_gateway
        self._achievement_gateway = achievement_gateway

    async def process(
        self,
        command: AcceptMovieEditingCommand,
    ) -> Optional[AchievementId]:
        contribution = (
            await self._edit_movie_contribution_gateway.acquire_by_id(
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

        movie = await self._movie_gateway.acquire_by_id(
            id=contribution.movie_id,
        )
        if not movie:
            raise MovieDoesNotExistError()

        achievement = self._accept_contribution(
            achievement_id=AchievementId(uuid7()),
            contribution=contribution,
            author=author,
            current_timestamp=command.accepted_at,
        )
        if achievement:
            await self._achievement_gateway.save(achievement)

        await self._user_gateway.update(author)
        await self._edit_movie_contribution_gateway.update(contribution)

        self._update_movie(
            movie,
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

        await self._delete_roles(list(contribution.remove_roles))
        await self._delete_writers(list(contribution.remove_writers))
        await self._delete_crew(list(contribution.remove_crew))

        return achievement.id if achievement else None


class LoggingProcessor:
    def __init__(
        self,
        *,
        processor: TransactionProcessor,
        correlation_id: CorrelationId,
    ):
        self._processor = processor
        self._correlation_id = correlation_id

    async def process(
        self,
        command: AcceptMovieEditingCommand,
    ) -> Optional[AchievementId]:
        logger.debug(
            "'Accept Movie Editing' command processing started",
            extra={
                "correlation_id": self._correlation_id,
                "command": command,
            },
        )

        try:
            result = await self._processor.process(command)
        except ContributionDoesNotExistError as e:
            logger.error(
                "Unexpected error occurred: Contribution doesn't exist",
                extra={"correlation_id": self._correlation_id},
            )
            raise e
        except UserDoesNotExistError as e:
            logger.error(
                "Unexpected error occurred: Contribution has author id, "
                "using which user gateway returns None",
                extra={"correlation_id": self._correlation_id},
            )
            raise e
        except MovieDoesNotExistError as e:
            logger.error(
                "Unexpected error occurred: Contribution has movie id,"
                "using which movie gateway returns None",
                extra={"correlation_id": self._correlation_id},
            )
            raise e
        except InvalidMovieEngTitleError as e:
            logger.error(
                "Unexpected error occurred: Invalid movie eng title",
                extra={"correlation_id": self._correlation_id},
            )
            raise e
        except InvalidMovieOriginalTitleError as e:
            logger.error(
                "Unexpected error occurred: Invalid movie original title",
                extra={"correlation_id": self._correlation_id},
            )
            raise e
        except InvalidMovieDurationError as e:
            logger.error(
                "Unexpected error occurred: Invalid movie duration",
                extra={"correlation_id": self._correlation_id},
            )
            raise e
        except RolesAlreadyExistError as e:
            logger.error(
                "Unexpected error occurred: "
                "Role ids already belong to some roles",
                extra={
                    "correlation_id": self._correlation_id,
                    "ids_of_existing_roles": e.ids_of_existing_roles,
                },
            )
            raise e
        except RolesDoNotExistError as e:
            logger.error(
                "Unexpected error occurred: "
                "Role ids do not belong to any roles",
                extra={
                    "correlation_id": self._correlation_id,
                    "ids_of_missing_roles": e.ids_of_missing_roles,
                },
            )
            raise e
        except WritersAlreadyExistError as e:
            logger.error(
                "Unexpected error occurred: "
                "Writer ids already belong to some writers",
                extra={
                    "correlation_id": self._correlation_id,
                    "ids_of_existing_writers": e.ids_of_existing_writers,
                },
            )
            raise e
        except WritersDoNotExistError as e:
            logger.error(
                "Unexpected error occurred: "
                "Writer ids do not belong to any writers",
                extra={
                    "correlation_id": self._correlation_id,
                    "ids_of_missing_writers": e.ids_of_missing_writers,
                },
            )
            raise e
        except CrewMembersAlreadyExistError as e:
            logger.error(
                "Unexpected error occurred: "
                "Crew member ids already belong to some crew members",
                extra={
                    "correlation_id": self._correlation_id,
                    "ids_of_existing_crew_members": e.ids_of_existing_crew_members,
                },
            )
            raise e
        except CrewMembersDoNotExistError as e:
            logger.error(
                "Unexpected error occurred: "
                "Crew member ids do not belong to any crew members",
                extra={
                    "correlation_id": self._correlation_id,
                    "ids_of_missing_crew_members": e.ids_of_missing_crew_members,
                },
            )
            raise e
        except PersonsDoNotExistError as e:
            logger.error(
                "Unexpected error occurred: "
                "Person ids referenced in contribution roles, writers or crew"
                "are do not belong to any persons",
                extra={
                    "correlation_id": self._correlation_id,
                    "ids_of_missing_persons": e.ids_of_missing_persons,
                },
            )
            raise e
        except AchievementDoesNotExistError as e:
            logger.error(
                "Unexpected error occurred: Achievement was created, "
                "but achievement gateway returns None",
                extra={"correlation_id": self._correlation_id},
            )
        except Exception as e:
            logger.exception(
                "Unexpected error occurred",
                exc_info=e,
                extra={
                    "correlation_id": self._correlation_id,
                    "error": e,
                },
            )
            raise e

        logger.debug(
            "'Accept Movie Editing' command processing completed",
            extra={
                "correlation_id": self._correlation_id,
                "achievement_id": result,
            },
        )

        return result
