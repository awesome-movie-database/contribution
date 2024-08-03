from typing import Collection

from contribution.domain import RoleId
from contribution.application.common.exceptions import RolesDoNotExistError
from contribution.application.common.gateways import RoleGateway


class DeleteRoles:
    def __init__(self, role_gateway: RoleGateway):
        self._role_gateway = role_gateway

    async def __call__(self, role_ids: Collection[RoleId]) -> None:
        await self._ensure_roles_exist(role_ids)

        roles = await self._role_gateway.list_by_ids(role_ids)
        await self._role_gateway.delete_many(roles)

    async def _ensure_roles_exist(
        self,
        role_ids: Collection[RoleId],
    ) -> None:
        roles = await self._role_gateway.list_by_ids(role_ids)

        some_of_roles_are_missing = len(role_ids) != len(roles)
        if some_of_roles_are_missing:
            ids_of_roles_from_gateway = [role.id for role in roles]
            non_existing_role_ids = set(role_ids).difference(
                ids_of_roles_from_gateway,
            )
            raise RolesDoNotExistError(non_existing_role_ids)
