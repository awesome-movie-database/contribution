from typing import Protocol, Optional
from datetime import date, datetime

from contribution.domain.value_objects import (
    EditPersonContributionId,
    UserId,
    PersonId,
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
        birth_date: Maybe[date],
        death_date: Maybe[Optional[date]],
        edited_at: datetime,
    ) -> None:
        raise NotImplementedError
