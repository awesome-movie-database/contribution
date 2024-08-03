from typing import Iterable

from uuid_extensions import uuid7

from contribution.domain import WriterId, MovieWriter
from contribution.application.common.value_objects import ContributionWriter


class CreateMovieWriters:
    def __call__(
        self,
        contribution_writers: Iterable[ContributionWriter],
    ) -> list[MovieWriter]:
        movie_writers = []
        for contribution_writer in contribution_writers:
            movie_writer = MovieWriter(
                id=WriterId(uuid7()),
                person_id=contribution_writer.person_id,
                writing=contribution_writer.writing,
            )
            movie_writers.append(movie_writer)

        return movie_writers
