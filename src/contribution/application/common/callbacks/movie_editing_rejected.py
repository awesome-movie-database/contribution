from typing import Protocol
from datetime import datetime

from contribution.domain.value_objects import EditMovieContributionId


class OnMovieEditingRejected(Protocol):
    async def __call__(
        self,
        *,
        id: EditMovieContributionId,
        rejected_at: datetime,
    ) -> None:
        raise NotImplementedError
