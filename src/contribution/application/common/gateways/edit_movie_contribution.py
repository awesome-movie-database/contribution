from typing import Protocol, Optional

from contribution.domain import (
    EditMovieContributionId,
    EditMovieContribution,
)


class EditMovieContributionGateway(Protocol):
    async def acquire_by_id(
        self,
        id: EditMovieContributionId,
    ) -> Optional[EditMovieContribution]:
        raise NotImplementedError

    async def save(self, contribution: EditMovieContribution) -> None:
        raise NotImplementedError

    async def update(self, contribution: EditMovieContribution) -> None:
        raise NotImplementedError
