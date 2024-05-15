from typing import Sequence

from contribution.domain import (
    CrewMemberId,
    Movie,
    CreateCrewMember,
)
from contribution.application.common.value_objects import MovieCrewMember
from contribution.application.common.exceptions import (
    CrewMembersAlreadyExistError,
)
from contribution.application.common.gateways import (
    PersonGateway,
    CrewMemberGateway,
)


class CreateAndSaveCrew:
    def __init__(
        self,
        create_crew_member: CreateCrewMember,
        person_gateway: PersonGateway,
        crew_member_gateway: CrewMemberGateway,
    ):
        self._create_crew_member = create_crew_member
        self._person_gateway = person_gateway
        self._crew_member_gateway = crew_member_gateway

    async def __call__(
        self,
        *,
        movie: Movie,
        movie_crew: Sequence[MovieCrewMember],
    ) -> None:
        movie_crew_members_ids = [
            movie_crew_member.id for movie_crew_member in movie_crew
        ]
        await self._ensure_crew_members_do_not_exist(
            *movie_crew_members_ids,
        )

        person_ids_of_movie_crew_members = [
            movie_crew_member.person_id for movie_crew_member in movie_crew
        ]
        persons = await self._person_gateway.list_with_ids(
            *person_ids_of_movie_crew_members,
        )

        crew = []
        for movie_crew_member, person in zip(movie_crew, persons):
            crew_member = self._create_crew_member(
                id=movie_crew_member.id,
                movie=movie,
                person=person,
                membership=movie_crew_member.membership,
            )
            crew.append(crew_member)

        await self._crew_member_gateway.save_seq(crew)

    async def _ensure_crew_members_do_not_exist(
        self,
        *crew_members_ids: CrewMemberId,
    ) -> None:
        crew_members = await self._crew_member_gateway.list_with_ids(
            *crew_members_ids,
        )
        if crew_members:
            raise CrewMembersAlreadyExistError(
                [crew_member.id for crew_member in crew_members],
            )
