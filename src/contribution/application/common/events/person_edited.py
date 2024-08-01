from dataclasses import dataclass
from typing import Iterable, Optional
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
    photos_to_add: Iterable[PhotoUrl]
    edited_at: datetime
