from typing import Protocol, Optional, Sequence

from contribution.domain.value_objects import RoleId
from contribution.domain.entities import Role


class RoleGateway(Protocol):
    async def with_id(self, id: RoleId) -> Optional[Role]:
        raise NotImplementedError

    async def list_with_ids(self, *ids: RoleId) -> list[Role]:
        raise NotImplementedError

    async def save_seq(self, roles: Sequence[Role]) -> None:
        raise NotImplementedError

    async def update(self, role: Role) -> None:
        raise NotImplementedError