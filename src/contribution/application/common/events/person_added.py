from dataclasses import dataclass
from typing import Iterable, Optional
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
    photos: Iterable[PhotoUrl]
    added_at: datetime
