from typing import Sequence

from contribution.domain.value_objects import RoleId
from contribution.domain.entities import Movie
from contribution.domain.services import CreateRole
from contribution.application.common.value_objects import MovieRole
from contribution.application.common.exceptions import RolesAlreadyExistError
from contribution.application.common.gateways import PersonGateway, RoleGateway


class CreateAndSaveRoles:
    def __init__(
        self,
        create_role: CreateRole,
        person_gateway: PersonGateway,
        role_gateway: RoleGateway,
    ):
        self._create_role = create_role
        self._person_gateway = person_gateway
        self._role_gateway = role_gateway

    async def __call__(
        self,
        *,
        movie: Movie,
        movie_roles: Sequence[MovieRole],
    ) -> None:
        movie_roles_ids = [movie_role.id for movie_role in movie_roles]
        await self._ensure_roles_do_not_exist(*movie_roles_ids)

        person_ids_of_movie_roles = [
            movie_role.person_id for movie_role in movie_roles
        ]
        persons = await self._person_gateway.list_with_ids(
            *person_ids_of_movie_roles,
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

        await self._role_gateway.save_seq(roles)

    async def _ensure_roles_do_not_exist(self, *roles_ids: RoleId) -> None:
        roles = await self._role_gateway.list_with_ids(*roles_ids)
        if roles:
            raise RolesAlreadyExistError([role.id for role in roles])
