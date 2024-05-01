from typing import Protocol
from datetime import datetime

from contribution.domain.value_objects import (
    AddMovieContributionId,
    UserId,
)


class OnMovieAdditionAccepted(Protocol):
    async def __call__(
        self,
        *,
        id: AddMovieContributionId,
        user_id: UserId,
        accepted_at: datetime,
    ) -> None:
        raise NotImplementedError
