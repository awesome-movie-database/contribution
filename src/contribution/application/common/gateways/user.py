from typing import Protocol, Optional

from contribution.domain.value_objects import (
    UserId,
    Email,
    Telegram,
)
from contribution.domain.entities import User


class UserGateway(Protocol):
    async def with_id(self, id: UserId) -> Optional[User]:
        raise NotImplementedError

    async def with_name(self, name: str) -> Optional[User]:
        raise NotImplementedError

    async def with_email(self, email: Email) -> Optional[User]:
        raise NotImplementedError

    async def with_telegram(self, telegram: Telegram) -> Optional[User]:
        raise NotImplementedError

    async def acquire_with_id(self, id: UserId) -> Optional[User]:
        raise NotImplementedError

    async def save(self, user: User) -> None:
        raise NotImplementedError

    async def update(self, user: User) -> None:
        raise NotImplementedError
