from typing import Sequence

from contribution.domain import RoleId
from contribution.application.common.exceptions import RolesDoNotExistError
from contribution.application.common.gateways import RoleGateway


class DeleteRoles:
    def __init__(self, role_gateway: RoleGateway):
        self._role_gateway = role_gateway

    async def __call__(self, roles_ids: Sequence[RoleId]) -> None:
        await self._ensure_roles_exist(roles_ids)

        roles = await self._role_gateway.list_with_ids(*roles_ids)
        await self._role_gateway.delete_seq(roles)

    async def _ensure_roles_exist(
        self,
        roles_ids: Sequence[RoleId],
    ) -> None:
        roles = await self._role_gateway.list_with_ids(*roles_ids)
        some_of_roles_are_missing = len(roles_ids) != len(roles)

        if some_of_roles_are_missing:
            ids_of_missing_roles = set(roles_ids).difference(
                [role.id for role in roles],
            )
            raise RolesDoNotExistError(list(ids_of_missing_roles))
