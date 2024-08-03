from dataclasses import dataclass
from typing import Optional

from contribution.domain import UserId


@dataclass(frozen=True, slots=True)
class CreateUserCommand:
    id: UserId
    name: str
    email: Optional[str]
    telegram: Optional[str]
    is_active: bool
