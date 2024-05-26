from typing import Protocol, Optional

from contribution.domain import MovieId, Movie


class MovieGateway(Protocol):
    async def by_id(self, id: MovieId) -> Optional[Movie]:
        raise NotImplementedError

    async def acquire_by_id(self, id: MovieId) -> Optional[Movie]:
        raise NotImplementedError

    async def save(self, movie: Movie) -> None:
        raise NotImplementedError

    async def update(self, movie: Movie) -> None:
        raise NotImplementedError
