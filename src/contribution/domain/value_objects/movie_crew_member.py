from dataclasses import dataclass

from contribution.domain.constants import CrewMembership
from .crew_member_id import CrewMemberId
from .person_id import PersonId


@dataclass(frozen=True, slots=True)
class MovieCrewMember:
    id: CrewMemberId
    person_id: PersonId
    membership: CrewMembership
