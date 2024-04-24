from dataclasses import dataclass

from contribution.domain.value_objects import UserId


@dataclass(slots=True)
class User:
    id: UserId
    name: str
    is_active: bool
    rating: float
    contributions_count: int
