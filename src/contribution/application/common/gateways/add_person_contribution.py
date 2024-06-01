from typing import Protocol, Optional

from contribution.domain import (
    AddPersonContributionId,
    AddPersonContribution,
)


class AddPersonContributionGateway(Protocol):
    async def acquire_by_id(
        self,
        id: AddPersonContributionId,
    ) -> Optional[AddPersonContribution]:
        raise NotImplementedError

    async def save(self, contribution: AddPersonContribution) -> None:
        raise NotImplementedError

    async def update(self, contribution: AddPersonContribution) -> None:
        raise NotImplementedError
