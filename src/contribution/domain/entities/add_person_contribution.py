from dataclasses import dataclass
from typing import Optional, Sequence
from datetime import date

from contribution.domain.value_objects import (
    AddPersonContributionId,
    UserId,
    PhotoUrl,
)
from .contribution import Contribution


@dataclass(slots=True)
class AddPersonContribution(Contribution):
    id: AddPersonContributionId
    author_id: UserId
    first_name: str
    last_name: str
    birth_date: date
    death_date: Optional[date]
    photos: Sequence[PhotoUrl]
