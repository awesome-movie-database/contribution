from dataclasses import dataclass

from contribution.domain.value_objects import PersonId


@dataclass(slots=True)
class ContributionRole:
    person_id: PersonId
    character: str
    importance: int
    is_spoiler: bool
