from typing import Protocol
from datetime import datetime

from contribution.domain.value_objects import EditMovieContributionId


class OnMovieEditingAccepted(Protocol):
    async def __call__(
        self,
        *,
        id: EditMovieContributionId,
        accepted_at: datetime,
    ) -> None:
        raise NotImplementedError
