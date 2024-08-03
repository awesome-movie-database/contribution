from typing import Iterable

from contribution.domain import (
    MovieCrewMember,
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
        movie_crew: Iterable[MovieCrewMember],
    ) -> None:
        await self._ensure_crew_members_do_not_exist(movie_crew)
        persons = await self._list_movie_crew_member_persons(movie_crew)

        crew = []
        for movie_crew_member, person in zip(movie_crew, persons):
            crew_member = self._create_crew_member(
                id=movie_crew_member.id,
                movie=movie,
                person=person,
                membership=movie_crew_member.membership,
            )
            crew.append(crew_member)

        await self._crew_member_gateway.save_many(crew)

    async def _ensure_crew_members_do_not_exist(
        self,
        movie_crew: Iterable[MovieCrewMember],
    ) -> None:
        crew_member_ids = [crew_member.id for crew_member in movie_crew]
        crew = await self._crew_member_gateway.list_by_ids(crew_member_ids)
        if crew:
            raise CrewMembersAlreadyExistError(
                [crew_member.id for crew_member in crew],
            )

    async def _list_movie_crew_member_persons(
        self,
        movie_crew: Iterable[MovieCrewMember],
    ) -> list[Person]:
        person_ids = [crew_member.person_id for crew_member in movie_crew]
        persons = await self._person_gateway.list_by_ids(person_ids)

        some_persons_are_missing = len(person_ids) != len(persons)

        if some_persons_are_missing:
            ids_of_persons_from_gateway = [person for person in persons]
            ids_of_missing_persons = set(person_ids).difference(
                ids_of_persons_from_gateway,
            )
            raise PersonsDoNotExistError(ids_of_missing_persons)

        return persons
