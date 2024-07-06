from typing import Any, Iterable, Mapping, Optional
from uuid import UUID

from motor.motor_asyncio import AsyncIOMotorClientSession

from contribution.domain import (
    Writing,
    WriterId,
    MovieId,
    PersonId,
    Writer,
)
from contribution.infrastructure.database.collections import (
    WriterCollection,
)
from contribution.infrastructure.database.identity_maps import (
    WriterMap,
)
from contribution.infrastructure.database.unit_of_work import (
    MongoDBUnitOfWork,
)


class WriterMapper:
    def __init__(
        self,
        writer_map: WriterMap,
        writer_collection: WriterCollection,
        unit_of_work: MongoDBUnitOfWork,
        session: AsyncIOMotorClientSession,
    ):
        self._writer_map = writer_map
        self._writer_collection = writer_collection
        self._unit_of_work = unit_of_work
        self._session = session

    async def by_id(self, id: WriterId) -> Optional[Writer]:
        writer_from_map = self._writer_map.by_id(id)
        if writer_from_map:
            return writer_from_map

        document = await self._writer_collection.find_one(
            {"id": id.hex},
            session=self._session,
        )
        if document:
            role = self._document_to_writer(document)
            self._writer_map.save(role)
            self._unit_of_work.register_clean(role)
            return role

        return None

    async def list_by_ids(
        self,
        ids: Iterable[WriterId],
    ) -> list[Writer]:
        writers_from_map = []
        for id in ids:
            writer_from_map = self._writer_map.by_id(id)
            if not writer_from_map:
                break
            writers_from_map.append(writer_from_map)
        else:
            return writers_from_map

        documents = await self._writer_collection.find(
            {"id": {"$in": [id.hex for id in ids]}},
            session=self._session,
        ).to_list(None)

        writers = []
        for document in documents:
            role = self._document_to_writer(document)
            self._writer_map.save(role)
            self._unit_of_work.register_clean(role)
            writers.append(role)

        return writers

    async def save_many(self, writers: Iterable[Writer]) -> None:
        for writer in writers:
            self._writer_map.save(writer)
            self._unit_of_work.register_new(writer)

    async def update(self, writer: Writer) -> None:
        self._unit_of_work.register_dirty(writer)

    async def delete_many(self, writers: Iterable[Writer]) -> None:
        for writer in writers:
            self._unit_of_work.register_deleted(writer)

    def _document_to_writer(self, document: Mapping[str, Any]) -> Writer:
        return Writer(
            id=WriterId(UUID(document["id"])),
            movie_id=MovieId(UUID(document["movie_id"])),
            person_id=PersonId(UUID(document["person_id"])),
            writing=Writing(document["writing"]),
        )
