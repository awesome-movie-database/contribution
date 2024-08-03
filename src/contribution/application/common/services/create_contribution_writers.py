from typing import Iterable

from uuid_extensions import uuid7

from contribution.domain import WriterId, ContributionWriter
from contribution.application.common.value_objects import MovieWriter


class CreateContributionWriters:
    def __call__(
        self,
        movie_writers: Iterable[MovieWriter],
    ) -> list[ContributionWriter]:
        contribution_writers = []
        for movie_writer in movie_writers:
            contribution_writer = ContributionWriter(
                id=WriterId(uuid7()),
                person_id=movie_writer.person_id,
                writing=movie_writer.writing,
            )
            contribution_writers.append(contribution_writer)

        return contribution_writers
