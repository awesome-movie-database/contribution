from dataclasses import dataclass
from typing import Optional

from contribution.domain import MovieId, Movie


@dataclass(slots=True, unsafe_hash=True)
class MovieMapUnit:
    movie: Movie
    is_acquired: bool


class MovieMap:
    def __init__(self):
        self._units: set[MovieMapUnit] = set()

    def by_id(self, id: MovieId) -> Optional[Movie]:
        for unit in self._units:
            if unit.movie.id == id:
                return unit.movie
        return None

    def save(self, movie: Movie) -> None:
        """
        Saves movie in identity map if movie doesn't
        exist, otherwise raises ValueError.
        """
        movie_from_map = self.by_id(movie.id)
        if movie_from_map:
            message = "Movie already exists in identity map"
            raise ValueError(message)
        unit = MovieMapUnit(movie=movie, is_acquired=False)
        self._units.add(unit)

    def save_acquired(self, movie: Movie) -> None:
        """
        Saves movie as acquired in identity map if movie
        doesn't exist or already exist and not marked as
        acquired, otherwise raises ValueError.
        """
        movie_from_map = self.by_id(movie.id)
        if not movie_from_map:
            unit = MovieMapUnit(movie=movie, is_acquired=True)
            self._units.add(unit)

        movie_is_acquired = self.is_acquired(movie)
        if movie_is_acquired:
            message = (
                "Movie already exists in identity map and marked as acquired"
            )
            raise ValueError(message)

        for unit in self._units:
            if unit.movie == movie:
                unit.is_acquired = True
                return

    def is_acquired(self, movie: Movie) -> bool:
        """
        Returns whether movie is acquired if movie exists
        in identity map, otherwise raises ValueError.
        """
        for unit in self._units:
            if unit.movie == movie:
                return unit.is_acquired
        message = "Movie doesn't exist in identity map"
        raise ValueError(message)
