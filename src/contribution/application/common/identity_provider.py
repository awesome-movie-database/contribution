from typing import Protocol

from contribution.domain import UserId


class IdentityProvider(Protocol):
    async def user_id(self) -> UserId:
        raise NotImplementedError

    async def permissions(self) -> int:
        raise NotImplementedError
