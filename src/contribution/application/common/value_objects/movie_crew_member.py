from dataclasses import dataclass

from contribution.domain import (
    CrewMembership,
    CrewMemberId,
    PersonId,
)


@dataclass(frozen=True, slots=True)
class MovieCrewMember:
    id: CrewMemberId
    person_id: PersonId
    membership: CrewMembership
