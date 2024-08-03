from dataclasses import dataclass

from contribution.domain import CrewMembership, PersonId


@dataclass(frozen=True, slots=True)
class MovieCrewMember:
    person_id: PersonId
    membership: CrewMembership
