from dataclasses import dataclass

from contribution.domain.constants import CrewMembership
from .person_id import PersonId


@dataclass(frozen=True, slots=True)
class ContributionCrewMember:
    person_id: PersonId
    membership: CrewMembership
