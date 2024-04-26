from dataclasses import dataclass
from typing import Optional

from contribution.domain.value_objects import (
    UserId,
    Email,
    Telegram,
)


@dataclass(frozen=True, slots=True)
class UpdateUserCommand:
    user_id: UserId
    name: str
    email: Optional[Email]
    telegram: Optional[Telegram]
    is_active: bool
