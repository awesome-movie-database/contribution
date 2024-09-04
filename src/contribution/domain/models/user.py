from dataclasses import dataclass
from typing import Optional

from contribution.domain.value_objects import UserId


@dataclass(slots=True)
class User:
    id: UserId
    name: str
    email: Optional[str]
    telegram: Optional[str]
    is_active: bool
    rating: float
    accepted_contributions_count: int
    rejected_contributions_count: int
