from typing import Protocol
from datetime import datetime

from contribution.domain.value_objects import EditPersonContributionId


class OnPersonEditingAccepted(Protocol):
    async def __call__(
        self,
        *,
        id: EditPersonContributionId,
        accepted_at: datetime,
    ) -> None:
        raise NotImplementedError
