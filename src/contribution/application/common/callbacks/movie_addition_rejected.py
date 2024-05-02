from typing import Protocol
from datetime import datetime

from contribution.domain.value_objects import AddMovieContributionId


class OnMovieAdditionRejected(Protocol):
    async def __call__(
        self,
        *,
        id: AddMovieContributionId,
        rejected_at: datetime,
    ) -> None:
        raise NotImplementedError
