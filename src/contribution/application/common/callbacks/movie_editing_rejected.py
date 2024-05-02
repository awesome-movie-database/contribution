from typing import Protocol
from datetime import datetime

from contribution.domain.value_objects import (
    EditMovieContributionId,
    UserId,
)


class OnMovieEditingRejected(Protocol):
    async def __call__(
        self,
        *,
        id: EditMovieContributionId,
        user_id: UserId,
        movie_title: str,
        rejected_at: datetime,
    ) -> None:
        raise NotImplementedError
