from contribution.domain.value_objects import CrewMemberId
from contribution.application.common.exceptions import (
    CrewMembersAlreadyExistError,
)
from contribution.application.common.gateways import CrewMemberGateway


class EnsureCrewMembersDoNotExist:
    def __init__(self, crew_member_gateway: CrewMemberGateway):
        self._crew_member_gateway = crew_member_gateway

    async def __call__(self, *crew_members_ids: CrewMemberId) -> None:
        crew_members_from_gateway = await self._crew_member_gateway.list_with_ids(
            *crew_members_ids,
        )
        if crew_members_from_gateway:
            ids_of_crew_members_from_gateway = [
                crew_member_from_gateway.id
                for crew_member_from_gateway in crew_members_from_gateway
            ]
            raise CrewMembersAlreadyExistError(
                ids_of_existing_crew_members=ids_of_crew_members_from_gateway,
            )
