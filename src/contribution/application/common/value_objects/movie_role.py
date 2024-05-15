from dataclasses import dataclass

from contribution.domain import RoleId, PersonId


@dataclass(frozen=True, slots=True)
class MovieRole:
    id: RoleId
    person_id: PersonId
    character: str
    importance: int
    is_spoiler: bool
