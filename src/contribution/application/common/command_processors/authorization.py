from contribution.application.common.services import AccessConcern
from contribution.application.common.exceptions import (
    NotEnoughPermissionsError,
)
from contribution.application.common.gateways import PermissionsGateway
from contribution.application.common.identity_provider import IdentityProvider
from .command import CommandProcessor


class AuthorizationProcessor[C, R]:
    def __init__(
        self,
        *,
        processor: CommandProcessor[C, R],
        access_concern: AccessConcern,
        permissions_gateway: PermissionsGateway,
        identity_provider: IdentityProvider,
    ):
        self._processor = processor
        self._access_concern = access_concern
        self._permissions_gateway = permissions_gateway
        self._identity_provider = identity_provider

    async def process(self, command: C) -> R:
        current_user_permissions = await self._identity_provider.permissions()
        required_permissions = (
            await self._permissions_gateway.for_contribution()
        )

        access = self._access_concern.authorize(
            current_user_permissions,
            required_permissions,
        )
        if not access:
            raise NotEnoughPermissionsError()

        return await self._processor.process(command)
