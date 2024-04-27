from datetime import datetime, timezone
from typing import Sequence

from uuid_extensions import uuid7

from contribution.domain.value_objects import (
    EditMovieContributionId,
    RoleId,
    WriterId,
    CrewMemberId,
)
from contribution.domain.services import EditMovie
from contribution.application.common.services import (
    AccessConcern,
    EnsurePersonsExist,
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
from contribution.application.common.unit_of_work import UnitOfWork
from contribution.application.common.identity_provider import IdentityProvider
from contribution.application.commands import EditMovieCommand


def edit_movie_factory(
    edit_movie: EditMovie,
    access_concern: AccessConcern,
    ensure_persons_exist: EnsurePersonsExist,
    edit_movie_contribution_gateway: EditMovieContributionGateway,
    user_gateway: UserGateway,
    movie_gateway: MovieGateway,
    role_gateway: RoleGateway,
    writer_gateway: WriterGateway,
    crew_member_gateway: CrewMemberGateway,
    permissions_gateway: PermissionsGateway,
    unit_of_work: UnitOfWork,
    identity_provider: IdentityProvider,
) -> CommandProcessor[EditMovieCommand, EditMovieContributionId]:
    edit_movie_processor = EditMovieProcessor(
        edit_movie=edit_movie,
        ensure_persons_exist=ensure_persons_exist,
        edit_movie_contribution_gateway=edit_movie_contribution_gateway,
        user_gateway=user_gateway,
        movie_gateway=movie_gateway,
        role_gateway=role_gateway,
        writer_gateway=writer_gateway,
        crew_member_gateway=crew_member_gateway,
        identity_provider=identity_provider,
    )
    authz_processor = AuthorizationProcessor(
        processor=edit_movie_processor,
        access_concern=access_concern,
        permissions_gateway=permissions_gateway,
        identity_provider=identity_provider,
    )
    tx_processor = TransactionProcessor(
        processor=authz_processor,
        unit_of_work=unit_of_work,
    )
    return tx_processor


class EditMovieProcessor:
    def __init__(
        self,
        *,
        edit_movie: EditMovie,
        ensure_persons_exist: EnsurePersonsExist,
        edit_movie_contribution_gateway: EditMovieContributionGateway,
        user_gateway: UserGateway,
        movie_gateway: MovieGateway,
        role_gateway: RoleGateway,
        writer_gateway: WriterGateway,
        crew_member_gateway: CrewMemberGateway,
        identity_provider: IdentityProvider,
    ):
        self._edit_movie = edit_movie
        self._ensure_persons_exist = ensure_persons_exist
        self._edit_movie_contribution_gateway = edit_movie_contribution_gateway
        self._user_gateway = user_gateway
        self._movie_gateway = movie_gateway
        self._role_gateway = role_gateway
        self._writer_gateway = writer_gateway
        self._crew_member_gateway = crew_member_gateway
        self._identity_provider = identity_provider

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

        contribution = self._edit_movie(
            id=EditMovieContributionId(uuid7()),
            author=author,
            movie=movie,
            title=command.title,
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
            current_timestamp=datetime.now(timezone.utc),
        )
        await self._edit_movie_contribution_gateway.save(contribution)

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
