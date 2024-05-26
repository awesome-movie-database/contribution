from typing import Iterable, Protocol, Optional

from contribution.domain import (
    CrewMemberId,
    CrewMember,
)


class CrewMemberGateway(Protocol):
    async def by_id(self, id: CrewMemberId) -> Optional[CrewMember]:
        raise NotImplementedError

    async def list_by_ids(
        self,
        ids: Iterable[CrewMemberId],
    ) -> list[CrewMember]:
        raise NotImplementedError

    async def save_many(self, crew_members: Iterable[CrewMember]) -> None:
        raise NotImplementedError

    async def update(self, crew_member: CrewMember) -> None:
        raise NotImplementedError

    async def delete_many(self, crew_members: Iterable[CrewMember]) -> None:
        raise NotImplementedError
