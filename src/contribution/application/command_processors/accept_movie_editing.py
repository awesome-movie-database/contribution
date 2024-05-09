import logging
from typing import Optional, Sequence

from uuid_extensions import uuid7

from contribution.domain.value_objects import (
    AchievementId,
    RoleId,
    WriterId,
    CrewMemberId,
)
from contribution.domain.exceptions import (
    InvalidMovieEngTitleError,
    InvalidMovieOriginalTitleError,
    InvalidMovieDurationError,
)
from contribution.domain.services import (
    AcceptContribution,
    UpdateMovie,
)
from contribution.application.common.services import (
    CreateRoles,
    CreateWriters,
    CreateCrew,
)
from contribution.application.common.command_processors import (
    CommandProcessor,
    TransactionProcessor,
    AchievementEearnedCallbackProcessor,
)
from contribution.application.common.exceptions import (
    MovieDoesNotExistError,
    UserDoesNotExistError,
    ContributionDoesNotExistError,
    RolesAlreadyExistError,
    RolesDoNotExistError,
    WritersAlreadyExistError,
    WritersDoNotExistError,
    CrewMembersAlreadyExistError,
    CrewMembersDoNotExistError,
    AchievementDoesNotExistError,
)
from contribution.application.common.gateways import (
    EditMovieContributionGateway,
    MovieGateway,
    RoleGateway,
    WriterGateway,
    CrewMemberGateway,
    UserGateway,
    AchievementGateway,
)
from contribution.application.common.unit_of_work import UnitOfWork
from contribution.application.common.callbacks import OnAchievementEarned
from contribution.application.commands import AcceptMovieEditingCommand


logger = logging.getLogger(__name__)


def accept_movie_editing_factory(
    accept_contribution: AcceptContribution,
    update_movie: UpdateMovie,
    create_roles: CreateRoles,
    create_writers: CreateWriters,
    create_crew: CreateCrew,
    edit_movie_contribution_gateway: EditMovieContributionGateway,
    user_gateway: UserGateway,
    movie_gateway: MovieGateway,
    role_gateway: RoleGateway,
    writer_gateway: WriterGateway,
    crew_member_gateway: CrewMemberGateway,
    achievement_gateway: AchievementGateway,
    unit_of_work: UnitOfWork,
    on_achievement_earned: OnAchievementEarned,
) -> CommandProcessor[AcceptMovieEditingCommand, Optional[AchievementId]]:
    accept_movie_editing_processor = AcceptMovieEditingProcessor(
        accept_contribution=accept_contribution,
        update_movie=update_movie,
        create_roles=create_roles,
        create_writers=create_writers,
        create_crew=create_crew,
        edit_movie_contribution_gateway=edit_movie_contribution_gateway,
        user_gateway=user_gateway,
        movie_gateway=movie_gateway,
        role_gateway=role_gateway,
        writer_gateway=writer_gateway,
        crew_member_gateway=crew_member_gateway,
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
    )

    return log_processor


class AcceptMovieEditingProcessor:
    def __init__(
        self,
        *,
        accept_contribution: AcceptContribution,
        update_movie: UpdateMovie,
        create_roles: CreateRoles,
        create_writers: CreateWriters,
        create_crew: CreateCrew,
        edit_movie_contribution_gateway: EditMovieContributionGateway,
        user_gateway: UserGateway,
        movie_gateway: MovieGateway,
        role_gateway: RoleGateway,
        writer_gateway: WriterGateway,
        crew_member_gateway: CrewMemberGateway,
        achievement_gateway: AchievementGateway,
    ):
        self._accept_contribution = accept_contribution
        self._update_movie = update_movie
        self._create_roles = create_roles
        self._create_writers = create_writers
        self._create_crew = create_crew
        self._edit_movie_contribution_gateway = edit_movie_contribution_gateway
        self._user_gateway = user_gateway
        self._movie_gateway = movie_gateway
        self._role_gateway = role_gateway
        self._writer_gateway = writer_gateway
        self._crew_member_gateway = crew_member_gateway
        self._achievement_gateway = achievement_gateway

    async def process(
        self,
        command: AcceptMovieEditingCommand,
    ) -> Optional[AchievementId]:
        contribution = await self._edit_movie_contribution_gateway.with_id(
            id=command.contribution_id,
        )
        if not contribution:
            raise ContributionDoesNotExistError()

        author = await self._user_gateway.acquire_with_id(
            id=contribution.author_id,
        )
        if not author:
            raise UserDoesNotExistError(contribution.author_id)

        movie = await self._movie_gateway.acquire_with_id(
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

        await self._ensure_roles_exist(contribution.remove_roles)
        await self._ensure_writers_exist(contribution.remove_writers)
        await self._ensure_crew_exist(contribution.remove_crew)

        roles = await self._role_gateway.list_with_ids(
            *contribution.remove_roles,
        )
        await self._role_gateway.delete_seq(roles)

        writers = await self._writer_gateway.list_with_ids(
            *contribution.remove_writers,
        )
        await self._writer_gateway.delete_seq(writers)

        crew_members = await self._crew_member_gateway.list_with_ids(
            *contribution.remove_crew,
        )
        await self._crew_member_gateway.delete_seq(crew_members)

        return achievement.id if achievement else None

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

    async def process(
        self,
        command: AcceptMovieEditingCommand,
    ) -> Optional[AchievementId]:
        command_processing_id = uuid7()

        logger.debug(
            "'Accept Movie Editing' command processing started",
            extra={
                "processing_id": command_processing_id,
                "command": command,
            },
        )

        try:
            result = await self._processor.process(command)
        except ContributionDoesNotExistError as e:
            logger.error(
                "Unexpected error occurred: Contribution doesn't exist",
                extra={"processing_id": command_processing_id},
            )
            raise e
        except UserDoesNotExistError as e:
            logger.error(
                "Unexpected error occurred: Contribution has author id, "
                "using which user gateway returns None",
                extra={"processing_id": command_processing_id},
            )
            raise e
        except MovieDoesNotExistError as e:
            logger.error(
                "Unexpected error occurred: Contribution has movie id,"
                "using which movie gateway returns None",
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
        except AchievementDoesNotExistError as e:
            logger.error(
                "Unexpected error occurred: Achievement was created, "
                "but achievement gateway returns None",
                extra={"processing_id": command_processing_id},
            )
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
            "'Accept Movie Editing' command processing completed",
            extra={
                "processing_id": command_processing_id,
                "achievement_id": result,
            },
        )

        return result
