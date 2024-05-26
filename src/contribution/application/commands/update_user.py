from dataclasses import dataclass
from typing import Optional

from contribution.domain import UserId, Maybe


@dataclass(frozen=True, slots=True)
class UpdateUserCommand:
    user_id: UserId
    name: Maybe[str]
    email: Maybe[Optional[str]]
    telegram: Maybe[Optional[str]]
    is_active: Maybe[bool]
