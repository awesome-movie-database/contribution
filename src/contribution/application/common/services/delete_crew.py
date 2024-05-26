from typing import Collection

from contribution.domain import CrewMemberId
from contribution.application.common.exceptions import (
    CrewMembersDoNotExistError,
)
from contribution.application.common.gateways import CrewMemberGateway


class DeleteCrew:
    def __init__(self, crew_member_gateway: CrewMemberGateway):
        self._crew_member_gateway = crew_member_gateway

    async def __call__(
        self,
        crew_member_ids: Collection[CrewMemberId],
    ) -> None:
        await self._ensure_crew_members_exist(crew_member_ids)

        crew_members = await self._crew_member_gateway.list_by_ids(
            crew_member_ids,
        )
        await self._crew_member_gateway.delete_many(crew_members)

    async def _ensure_crew_members_exist(
        self,
        crew_member_ids: Collection[CrewMemberId],
    ) -> None:
        crew_members = await self._crew_member_gateway.list_by_ids(
            crew_member_ids,
        )
        some_of_crew_members_are_missing = len(crew_member_ids) != len(
            crew_members,
        )

        if some_of_crew_members_are_missing:
            ids_of_missing_crew_members = set(crew_member_ids).difference(
                [crew_member.id for crew_member in crew_members],
            )
            raise CrewMembersDoNotExistError(list(ids_of_missing_crew_members))
