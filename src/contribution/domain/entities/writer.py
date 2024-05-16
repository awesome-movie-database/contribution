from dataclasses import dataclass

from contribution.domain.constants import Writing
from contribution.domain.value_objects import (
    WriterId,
    MovieId,
    PersonId,
)


@dataclass(slots=True, unsafe_hash=True)
class Writer:
    id: WriterId
    movie_id: MovieId
    person_id: PersonId
    writing: Writing
