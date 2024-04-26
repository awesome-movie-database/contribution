from typing import Protocol

from contribution.domain.entities import EditPersonContribution


class EditPersonContributionGateway(Protocol):
    async def save(self, contribution: EditPersonContribution) -> None:
        raise NotImplementedError

    async def update(self, contribution: EditPersonContribution) -> None:
        raise NotImplementedError
