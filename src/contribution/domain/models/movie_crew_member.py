from dataclasses import dataclass

from contribution.domain.constants import CrewMembership
from contribution.domain.value_objects import PersonId, CrewMemberId


@dataclass(frozen=True, slots=True)
class MovieCrewMember:
    id: CrewMemberId
    person_id: PersonId
    membership: CrewMembership
