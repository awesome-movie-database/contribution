from dataclasses import dataclass

from contribution.domain.constants import CrewMembership
from contribution.domain.value_objects import (
    CrewMemberId,
    MovieId,
    PersonId,
)


@dataclass(slots=True, unsafe_hash=True)
class CrewMember:
    id: CrewMemberId
    movie_id: MovieId
    person_id: PersonId
    membership: CrewMembership
