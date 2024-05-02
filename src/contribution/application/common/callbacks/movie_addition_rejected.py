from typing import Protocol
from datetime import datetime

from contribution.domain.value_objects import (
    AddMovieContributionId,
    UserId,
)


class OnMovieAdditionRejected(Protocol):
    async def __call__(
        self,
        *,
        id: AddMovieContributionId,
        user_id: UserId,
        movie_title: str,
        rejected_at: datetime,
    ) -> None:
        raise NotImplementedError
