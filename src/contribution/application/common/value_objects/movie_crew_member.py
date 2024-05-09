from dataclasses import dataclass

from contribution.domain.constants import CrewMembership
from contribution.domain.value_objects import (
    CrewMemberId,
    PersonId,
)


@dataclass(frozen=True, slots=True)
class MovieCrewMember:
    id: CrewMemberId
    person_id: PersonId
    membership: CrewMembership
