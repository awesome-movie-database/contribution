from typing import Iterable

from uuid_extensions import uuid7

from contribution.domain import CrewMemberId, ContributionCrewMember
from contribution.application.common.value_objects import MovieCrewMember


class CreateContributionCrew:
    def __call__(
        self,
        movie_crew: Iterable[MovieCrewMember],
    ) -> list[ContributionCrewMember]:
        contribution_crew_members = []
        for movie_crew_member in movie_crew:
            contribution_crew_member = ContributionCrewMember(
                id=CrewMemberId(uuid7()),
                person_id=movie_crew_member.person_id,
                membership=movie_crew_member.membership,
            )
            contribution_crew_members.append(contribution_crew_member)

        return contribution_crew_members
