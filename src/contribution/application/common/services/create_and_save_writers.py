from typing import Sequence

from contribution.domain import (
    WriterId,
    Movie,
    CreateWriter,
)
from contribution.application.common.value_objects import MovieWriter
from contribution.application.common.exceptions import WritersAlreadyExistError
from contribution.application.common.gateways import (
    PersonGateway,
    WriterGateway,
)


class CreateAndSaveWriters:
    def __init__(
        self,
        create_writer: CreateWriter,
        person_gateway: PersonGateway,
        writer_gateway: WriterGateway,
    ):
        self._create_writer = create_writer
        self._person_gateway = person_gateway
        self._writer_gateway = writer_gateway

    async def __call__(
        self,
        *,
        movie: Movie,
        movie_writers: Sequence[MovieWriter],
    ) -> None:
        movie_writers_ids = [movie_writer.id for movie_writer in movie_writers]
        await self._ensure_writers_do_not_exist(*movie_writers_ids)

        person_ids_of_movie_writers = [
            movie_writer.person_id for movie_writer in movie_writers
        ]
        persons = await self._person_gateway.list_with_ids(
            *person_ids_of_movie_writers,
        )

        writers = []
        for movie_writer, person in zip(movie_writers, persons):
            writer = self._create_writer(
                id=movie_writer.id,
                movie=movie,
                person=person,
                writing=movie_writer.writing,
            )
            writers.append(writer)

        await self._writer_gateway.save_seq(writers)

    async def _ensure_writers_do_not_exist(
        self,
        *writers_ids: WriterId,
    ) -> None:
        writers = await self._writer_gateway.list_with_ids(*writers_ids)
        if writers:
            raise WritersAlreadyExistError([writer.id for writer in writers])
