from dataclasses import dataclass

from contribution.domain.value_objects import (
    RoleId,
    MovieId,
    PersonId,
)


@dataclass(slots=True)
class Role:
    id: RoleId
    movie_id: MovieId
    person_id: PersonId
    character: str
    importance: int
    is_spoiler: bool
