from dataclasses import dataclass

from contribution.domain import PersonId


@dataclass(frozen=True, slots=True)
class MovieRole:
    person_id: PersonId
    character: str
    importance: int
    is_spoiler: bool
