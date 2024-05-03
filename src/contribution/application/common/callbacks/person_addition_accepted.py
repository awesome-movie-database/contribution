from typing import Protocol
from datetime import datetime

from contribution.domain.value_objects import AddPersonContributionId


class OnPersonAdditionAccepted(Protocol):
    async def __call__(
        self,
        *,
        id: AddPersonContributionId,
        accepted_at: datetime,
    ) -> None:
        raise NotImplementedError
