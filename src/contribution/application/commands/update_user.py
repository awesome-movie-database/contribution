from dataclasses import dataclass
from typing import Optional

from contribution.domain.value_objects import (
    UserId,
    Email,
    Telegram,
)
from contribution.domain.maybe import Maybe


@dataclass(frozen=True, slots=True)
class UpdateUserCommand:
    user_id: UserId
    name: Maybe[str]
    email: Maybe[Optional[Email]]
    telegram: Maybe[Optional[Telegram]]
    is_active: Maybe[bool]
