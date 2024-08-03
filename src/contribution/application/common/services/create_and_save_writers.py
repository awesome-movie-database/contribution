from typing import Iterable

from contribution.domain import (
    MovieWriter,
    Movie,
    Person,
    CreateWriter,
)
from contribution.application.common.exceptions import (
    WritersAlreadyExistError,
    PersonsDoNotExistError,
)
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
        movie_writers: Iterable[MovieWriter],
    ) -> None:
        await self._ensure_writers_do_not_exist(movie_writers)
        persons = await self._list_movie_writer_persons(movie_writers)

        writers = []
        for movie_writer, person in zip(movie_writers, persons):
            writer = self._create_writer(
                id=movie_writer.id,
                movie=movie,
                person=person,
                writing=movie_writer.writing,
            )
            writers.append(writer)

        await self._writer_gateway.save_many(writers)

    async def _ensure_writers_do_not_exist(
        self,
        movie_writers: Iterable[MovieWriter],
    ) -> None:
        writer_ids = [writer.id for writer in movie_writers]
        writers = await self._writer_gateway.list_by_ids(writer_ids)
        if writers:
            raise WritersAlreadyExistError([writer.id for writer in writers])

    async def _list_movie_writer_persons(
        self,
        movie_writers: Iterable[MovieWriter],
    ) -> list[Person]:
        person_ids = [writer.person_id for writer in movie_writers]
        persons = await self._person_gateway.list_by_ids(person_ids)

        some_persons_are_missing = len(person_ids) != len(persons)
        if some_persons_are_missing:
            ids_of_persons_from_gateway = [person.id for person in persons]
            missing_person_ids = set(person_ids).difference(
                ids_of_persons_from_gateway,
            )
            raise PersonsDoNotExistError(missing_person_ids)

        return persons
