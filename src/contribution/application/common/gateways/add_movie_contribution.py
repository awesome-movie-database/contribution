from typing import Protocol

from contribution.domain.entities import AddMovieContribution


class AddMovieContributionGateway(Protocol):
    async def save(self, contribution: AddMovieContribution) -> None:
        raise NotImplementedError

    async def update(self, contribution: AddMovieContribution) -> None:
        raise NotImplementedError
