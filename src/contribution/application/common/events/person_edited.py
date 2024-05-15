from dataclasses import dataclass
from typing import Optional, Sequence
from datetime import date, datetime

from contribution.domain import (
    Sex,
    EditPersonContributionId,
    UserId,
    PersonId,
    PhotoUrl,
    Maybe,
)


@dataclass(frozen=True, slots=True)
class PersonEditedEvent:
    contribution_id: EditPersonContributionId
    author_id: UserId
    person_id: PersonId
    first_name: Maybe[str]
    last_name: Maybe[str]
    sex: Maybe[Sex]
    birth_date: Maybe[date]
    death_date: Maybe[Optional[date]]
    add_photos: Sequence[PhotoUrl]
    edited_at: datetime
