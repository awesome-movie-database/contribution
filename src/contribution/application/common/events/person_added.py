from dataclasses import dataclass
from typing import Optional, Sequence
from datetime import date, datetime

from contribution.domain import (
    Sex,
    AddPersonContributionId,
    UserId,
    PhotoUrl,
)


@dataclass(frozen=True, slots=True)
class PersonAddedEvent:
    contribtion_id: AddPersonContributionId
    author_id: UserId
    first_name: str
    last_name: str
    sex: Sex
    birth_date: date
    death_date: Optional[date]
    photos: Sequence[PhotoUrl]
    added_at: datetime
