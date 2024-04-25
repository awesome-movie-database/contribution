from dataclasses import dataclass
from typing import Optional
from datetime import date

from contribution.domain.constants import ContributionStatus
from contribution.domain.value_objects import (
    AddPersonContributionId,
    UserId,
)


@dataclass(slots=True)
class AddPersonContribution:
    id: AddPersonContributionId
    author_id: UserId
    first_name: str
    last_name: str
    birth_date: date
    death_date: Optional[date]
    status: ContributionStatus
