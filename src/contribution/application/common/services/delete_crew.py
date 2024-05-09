from typing import Sequence

from contribution.domain.value_objects import CrewMemberId
from contribution.application.common.exceptions import (
    CrewMembersDoNotExistError,
)
from contribution.application.common.gateways import CrewMemberGateway


class DeleteCrew:
    def __init__(self, crew_member_gateway: CrewMemberGateway):
        self._crew_member_gateway = crew_member_gateway

    async def __call__(self, crew_members_ids: Sequence[CrewMemberId]) -> None:
        await self._ensure_crew_members_exist(crew_members_ids)

        crew_members = await self._crew_member_gateway.list_with_ids(
            *crew_members_ids,
        )
        await self._crew_member_gateway.delete_seq(crew_members)

    async def _ensure_crew_members_exist(
        self,
        crew_members_ids: Sequence[CrewMemberId],
    ) -> None:
        crew_members = await self._crew_member_gateway.list_with_ids(
            *crew_members_ids,
        )
        some_of_crew_members_are_missing = len(crew_members_ids) != len(
            crew_members,
        )

        if some_of_crew_members_are_missing:
            ids_of_missing_crew_members = set(crew_members_ids).difference(
                [crew_member.id for crew_member in crew_members],
            )
            raise CrewMembersDoNotExistError(list(ids_of_missing_crew_members))
