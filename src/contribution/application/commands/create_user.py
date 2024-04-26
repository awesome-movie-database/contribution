from dataclasses import dataclass
from typing import Optional

from contribution.domain.value_objects import (
    Email,
    Telegram,
)


@dataclass(frozen=True, slots=True)
class CreateUserCommand:
    name: str
    email: Optional[Email]
    telegram: Optional[Telegram]
    is_active: bool
