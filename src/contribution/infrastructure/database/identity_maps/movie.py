from typing import Optional

from contribution.domain import MovieId, Movie


class MovieMap:
    def __init__(self):
        self._movies: set[Movie] = set()

    def with_id(self, id: MovieId) -> Optional[Movie]:
        for movie in self._movies:
            if movie.id == id:
                return movie
        return None

    def save(self, movie: Movie) -> None:
        """
        Saves movie in identity map if movie doesn't
        exist, otherwise raises ValueError.
        """
        movie_from_map = self.with_id(movie.id)
        if movie_from_map:
            message = "Movie already exists in identity map"
            raise ValueError(message)
        self._movies.add(movie)
