from contribution.domain.value_objects import RoleId
from contribution.application.common.exceptions import RolesAlreadyExistError
from contribution.application.common.gateways import RoleGateway


class EnsureRolesDoNotExist:
    def __init__(self, role_gateway: RoleGateway):
        self._role_gateway = role_gateway

    async def __call__(self, *roles_ids: RoleId) -> None:
        roles_from_gateway = await self._role_gateway.list_with_ids(
            *roles_ids,
        )
        if roles_from_gateway:
            ids_of_roles_from_gateway = [
                role_from_gateway.id
                for role_from_gateway in roles_from_gateway
            ]
            raise RolesAlreadyExistError(
                ids_of_existing_roles=ids_of_roles_from_gateway,
            )
