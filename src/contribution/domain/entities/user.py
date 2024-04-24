from dataclasses import dataclass
from typing import Optional

from contribution.domain.value_objects import (
    UserId,
    Email,
    Telegram,
)


@dataclass(slots=True)
class User:
    id: UserId
    name: str
    email: Optional[Email]
    telegram: Optional[Telegram]
    is_active: bool
    rating: float
    contributions_count: int
