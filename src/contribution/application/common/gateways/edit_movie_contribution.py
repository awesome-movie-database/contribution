from typing import Protocol

from contribution.domain.entities import EditMovieContribution


class EditMovieContributionGateway(Protocol):
    async def save(self, contribution: EditMovieContribution) -> None:
        raise NotImplementedError

    async def update(self, contribution: EditMovieContribution) -> None:
        raise NotImplementedError
