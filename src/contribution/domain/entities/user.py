from dataclasses import dataclass
from typing import Optional

from contribution.domain.value_objects import (
    UserId,
    Email,
    Telegram,
)


@dataclass(slots=True, unsafe_hash=True)
class User:
    id: UserId
    name: str
    email: Optional[Email]
    telegram: Optional[Telegram]
    is_active: bool
    rating: float
    accepted_contributions_count: int
    rejected_contributions_count: int
