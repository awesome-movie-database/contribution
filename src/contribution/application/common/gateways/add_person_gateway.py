from typing import Protocol

from contribution.domain.entities import AddPersonContribution


class AddPersonContributionGateway(Protocol):
    async def save(self, contribution: AddPersonContribution) -> None:
        raise NotImplementedError

    async def update(self, contribution: AddPersonContribution) -> None:
        raise NotImplementedError
