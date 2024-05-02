from typing import Protocol, Optional, Sequence
from datetime import date, datetime

from contribution.domain.constants import Sex
from contribution.domain.value_objects import (
    EditPersonContributionId,
    UserId,
    PersonId,
    PhotoUrl,
)
from contribution.domain.maybe import Maybe


class OnPersonEdited(Protocol):
    async def __call__(
        self,
        *,
        id: EditPersonContributionId,
        author_id: UserId,
        person_id: PersonId,
        first_name: Maybe[str],
        last_name: Maybe[str],
        sex: Maybe[Sex],
        birth_date: Maybe[date],
        death_date: Maybe[Optional[date]],
        add_photos: Sequence[PhotoUrl],
        edited_at: datetime,
    ) -> None:
        raise NotImplementedError
