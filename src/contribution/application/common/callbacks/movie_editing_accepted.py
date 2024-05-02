from typing import Protocol
from datetime import datetime

from contribution.domain.value_objects import (
    EditMovieContributionId,
    UserId,
)


class OnMovieEditingAccepted(Protocol):
    async def __call__(
        self,
        *,
        id: EditMovieContributionId,
        user_id: UserId,
        movie_title: str,
        accepted_at: datetime,
    ) -> None:
        raise NotImplementedError
