from typing import Protocol, Optional

from contribution.domain import UserId


class IdentityProvider(Protocol):
    async def user_id(self) -> UserId:
        raise NotImplementedError

    async def user_id_or_none(self) -> Optional[UserId]:
        raise NotImplementedError

    async def permissions(self) -> int:
        raise NotImplementedError
