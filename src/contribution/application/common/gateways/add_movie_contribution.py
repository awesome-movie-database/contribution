from typing import Protocol, Optional

from contribution.domain import (
    AddMovieContributionId,
    AddMovieContribution,
)


class AddMovieContributionGateway(Protocol):
    async def acquire_with_id(
        self,
        id: AddMovieContributionId,
    ) -> Optional[AddMovieContribution]:
        raise NotImplementedError

    async def save(self, contribution: AddMovieContribution) -> None:
        raise NotImplementedError

    async def update(self, contribution: AddMovieContribution) -> None:
        raise NotImplementedError
