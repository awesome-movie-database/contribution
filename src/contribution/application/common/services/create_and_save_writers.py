from typing import Iterable

from contribution.domain import (
    WriterId,
    ContributionWriter,
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
        contribution_writers: Iterable[ContributionWriter],
    ) -> None:
        writer_ids = [writer.id for writer in contribution_writers]
        await self._ensure_writers_do_not_exist(writer_ids)

        persons = await self._list_persons_of_movie_writers(
            contribution_writers=contribution_writers,
        )

        writers = []
        for contribution_writer, person in zip(contribution_writers, persons):
            writer = self._create_writer(
                id=contribution_writer.id,
                movie=movie,
                person=person,
                writing=contribution_writer.writing,
            )
            writers.append(writer)

        await self._writer_gateway.save_many(writers)

    async def _ensure_writers_do_not_exist(
        self,
        writer_ids: Iterable[WriterId],
    ) -> None:
        writers = await self._writer_gateway.list_by_ids(writer_ids)
        if writers:
            raise WritersAlreadyExistError([writer.id for writer in writers])

    async def _list_persons_of_movie_writers(
        self,
        contribution_writers: Iterable[ContributionWriter],
    ) -> list[Person]:
        person_ids = [writer.person_id for writer in contribution_writers]
        persons = await self._person_gateway.list_by_ids(person_ids)

        some_persons_are_missing = len(person_ids) != len(persons)

        if some_persons_are_missing:
            ids_of_persons_from_gateway = [person for person in persons]
            ids_of_missing_persons = set(person_ids).difference(
                ids_of_persons_from_gateway,
            )
            raise PersonsDoNotExistError(ids_of_missing_persons)

        return persons
