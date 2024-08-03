from typing import Iterable

from contribution.domain import (
    CrewMemberId,
    ContributionCrewMember,
    Movie,
    Person,
    CreateCrewMember,
)
from contribution.application.common.exceptions import (
    CrewMembersAlreadyExistError,
    PersonsDoNotExistError,
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
        contribution_crew: Iterable[ContributionCrewMember],
    ) -> None:
        crew_member_ids = [crew_member.id for crew_member in contribution_crew]
        await self._ensure_crew_members_do_not_exist(crew_member_ids)

        persons = await self._list_persons_of_movie_crew(contribution_crew)

        crew = []
        for contribution_crew_member, person in zip(
            contribution_crew,
            persons,
        ):
            crew_member = self._create_crew_member(
                id=contribution_crew_member.id,
                movie=movie,
                person=person,
                membership=contribution_crew_member.membership,
            )
            crew.append(crew_member)

        await self._crew_member_gateway.save_many(crew)

    async def _ensure_crew_members_do_not_exist(
        self,
        crew_member_ids: Iterable[CrewMemberId],
    ) -> None:
        crew_members = await self._crew_member_gateway.list_by_ids(
            crew_member_ids,
        )
        if crew_members:
            raise CrewMembersAlreadyExistError(
                [crew_member.id for crew_member in crew_members],
            )

    async def _list_persons_of_movie_crew(
        self,
        contribution_crew: Iterable[ContributionCrewMember],
    ) -> list[Person]:
        person_ids = [
            crew_member.person_id for crew_member in contribution_crew
        ]
        persons = await self._person_gateway.list_by_ids(person_ids)

        some_persons_are_missing = len(person_ids) != len(persons)

        if some_persons_are_missing:
            ids_of_persons_from_gateway = [person for person in persons]
            ids_of_missing_persons = set(person_ids).difference(
                ids_of_persons_from_gateway,
            )
            raise PersonsDoNotExistError(ids_of_missing_persons)

        return persons
