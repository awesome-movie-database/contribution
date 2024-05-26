from typing import Protocol, Optional

from contribution.domain import UserId, User


class UserGateway(Protocol):
    async def with_id(self, id: UserId) -> Optional[User]:
        raise NotImplementedError

    async def with_name(self, name: str) -> Optional[User]:
        raise NotImplementedError

    async def with_email(self, email: str) -> Optional[User]:
        raise NotImplementedError

    async def with_telegram(self, telegram: str) -> Optional[User]:
        raise NotImplementedError

    async def acquire_with_id(self, id: UserId) -> Optional[User]:
        raise NotImplementedError

    async def save(self, user: User) -> None:
        raise NotImplementedError

    async def update(self, user: User) -> None:
        raise NotImplementedError
