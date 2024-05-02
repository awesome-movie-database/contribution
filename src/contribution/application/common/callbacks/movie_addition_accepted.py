from typing import Protocol
from datetime import datetime

from contribution.domain.value_objects import AddMovieContributionId


class OnMovieAdditionAccepted(Protocol):
    async def __call__(
        self,
        *,
        id: AddMovieContributionId,
        accepted_at: datetime,
    ) -> None:
        raise NotImplementedError
