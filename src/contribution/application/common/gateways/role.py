from typing import Iterable, Protocol, Optional

from contribution.domain import RoleId, Role


class RoleGateway(Protocol):
    async def by_id(self, id: RoleId) -> Optional[Role]:
        raise NotImplementedError

    async def list_by_ids(
        self,
        ids: Iterable[RoleId],
    ) -> list[Role]:
        raise NotImplementedError

    async def save_many(self, roles: Iterable[Role]) -> None:
        raise NotImplementedError

    async def update(self, role: Role) -> None:
        raise NotImplementedError

    async def delete_many(self, roles: Iterable[Role]) -> None:
        raise NotImplementedError
