from typing import Optional, cast

from fastapi import Request

from contribution.domain import UserId
from .permissions_storage import PermissionsStorage


def web_api_raw_identity_factory_provider_factory(
    request: Request,
    permissions_storage: PermissionsStorage,
) -> "RawIdentityProvider":
    user_id_as_str = request.headers.get("X-Current-User-Id", None)
    if user_id_as_str:
        user_id = UserId(user_id_as_str)
    else:
        user_id = None

    return RawIdentityProvider(
        user_id=user_id,
        permissions_storage=permissions_storage,
    )


class UserIsNotAuthenticatedError(Exception):
    ...


class RawIdentityProvider:
    def __init__(
        self,
        user_id: Optional[UserId],
        permissions_storage: PermissionsStorage,
    ):
        self._user_id = user_id
        self._permissions_storage = permissions_storage

    async def user_id(self) -> UserId:
        user_id = self._ensure_user_is_authenticated()
        return user_id

    async def permissions(self) -> int:
        user_id = self._ensure_user_is_authenticated()
        return await self._permissions_storage.get(user_id)

    async def for_contribution(self) -> int:
        return 2

    def _ensure_user_is_authenticated(self) -> UserId:
        if not self._user_id:
            raise UserIsNotAuthenticatedError()
        return cast(UserId, self._user_id)
