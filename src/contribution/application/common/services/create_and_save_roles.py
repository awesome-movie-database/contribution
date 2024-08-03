from typing import Iterable

from contribution.domain import (
    RoleId,
    ContributionRole,
    Movie,
    Person,
    CreateRole,
)
from contribution.application.common.exceptions import (
    RolesAlreadyExistError,
    PersonsDoNotExistError,
)
from contribution.application.common.gateways import (
    PersonGateway,
    RoleGateway,
)


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
        contribution_roles: Iterable[ContributionRole],
    ) -> None:
        role_ids = [role.id for role in contribution_roles]
        await self._ensure_roles_do_not_exist(role_ids)

        persons = await self._list_persons_of_movie_roles(contribution_roles)

        roles = []
        for contribution_role, person in zip(contribution_roles, persons):
            role = self._create_role(
                id=contribution_role.id,
                movie=movie,
                person=person,
                character=contribution_role.character,
                importance=contribution_role.importance,
                is_spoiler=contribution_role.is_spoiler,
            )
            roles.append(role)

        await self._role_gateway.save_many(roles)

    async def _ensure_roles_do_not_exist(
        self,
        role_ids: Iterable[RoleId],
    ) -> None:
        roles = await self._role_gateway.list_by_ids(role_ids)
        if roles:
            raise RolesAlreadyExistError([role.id for role in roles])

    async def _list_persons_of_movie_roles(
        self,
        contribution_roles: Iterable[ContributionRole],
    ) -> list[Person]:
        person_ids = [role.person_id for role in contribution_roles]
        persons = await self._person_gateway.list_by_ids(person_ids)

        some_persons_are_missing = len(person_ids) != len(persons)

        if some_persons_are_missing:
            ids_of_persons_from_gateway = [person for person in persons]
            ids_of_missing_persons = set(person_ids).difference(
                ids_of_persons_from_gateway,
            )
            raise PersonsDoNotExistError(ids_of_missing_persons)

        return persons
