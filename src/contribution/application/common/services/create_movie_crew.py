from typing import Iterable

from uuid_extensions import uuid7

from contribution.domain import CrewMemberId, MovieCrewMember
from contribution.application.common.value_objects import (
    ContributionCrewMember,
)


class CreateMovieCrew:
    def __call__(
        self,
        contribution_crew: Iterable[ContributionCrewMember],
    ) -> list[MovieCrewMember]:
        movie_crew = []
        for contribution_crew_member in contribution_crew:
            movie_crew_member = MovieCrewMember(
                id=CrewMemberId(uuid7()),
                person_id=contribution_crew_member.person_id,
                membership=contribution_crew_member.membership,
            )
            movie_crew.append(movie_crew_member)

        return movie_crew
