from typing import Protocol, Optional, Sequence

from contribution.domain import (
    CrewMemberId,
    CrewMember,
)


class CrewMemberGateway(Protocol):
    async def with_id(self, id: CrewMemberId) -> Optional[CrewMember]:
        raise NotImplementedError

    async def list_with_ids(self, *ids: CrewMemberId) -> list[CrewMember]:
        raise NotImplementedError

    async def save_seq(self, crew_members: Sequence[CrewMember]) -> None:
        raise NotImplementedError

    async def update(self, crew_member: CrewMember) -> None:
        raise NotImplementedError

    async def delete_seq(self, crew_members: Sequence[CrewMember]) -> None:
        raise NotImplementedError
