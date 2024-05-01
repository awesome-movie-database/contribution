from typing import Protocol, Optional

from contribution.domain.value_objects import AddMovieContributionId
from contribution.domain.entities import AddMovieContribution


class AddMovieContributionGateway(Protocol):
    async def with_id(
        self,
        id: AddMovieContributionId,
    ) -> Optional[AddMovieContribution]:
        raise NotImplementedError

    async def save(self, contribution: AddMovieContribution) -> None:
        raise NotImplementedError

    async def update(self, contribution: AddMovieContribution) -> None:
        raise NotImplementedError
