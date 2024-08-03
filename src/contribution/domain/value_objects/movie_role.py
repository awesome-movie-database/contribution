from dataclasses import dataclass

from .role_id import RoleId
from .person_id import PersonId


@dataclass(frozen=True, slots=True)
class MovieRole:
    id: RoleId
    person_id: PersonId
    character: str
    importance: int
    is_spoiler: bool
