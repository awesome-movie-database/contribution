from typing import Any, Sequence

from pymongo import InsertOne, UpdateOne, DeleteOne
from motor.motor_asyncio import AsyncIOMotorClientSession

from contribution.domain import Writer
from contribution.infrastructure.database.collections import (
    WriterCollection,
)


class CommitWriterCollectionChanges:
    def __init__(
        self,
        collection: WriterCollection,
        session: AsyncIOMotorClientSession,
    ):
        self._collection = collection
        self._session = session

    async def __call__(
        self,
        *,
        new: Sequence[Writer],
        clean: Sequence[Writer],
        dirty: Sequence[Writer],
        deleted: Sequence[Writer],
    ) -> None:
        inserts = [
            InsertOne(self._writer_to_document(writer)) for writer in new
        ]
        updates = [
            UpdateOne(
                {"id": clean_writer.id},
                self._pipeline_to_update_writer(clean_writer, dirty_writer),
            )
            for clean_writer, dirty_writer in zip(clean, dirty)
        ]
        deletes = [DeleteOne({"id": writer.id}) for writer in deleted]

        changes: list[InsertOne, UpdateOne, DeleteOne] = [
            *inserts,
            *updates,
            *deletes,
        ]
        if changes:
            await self._collection.bulk_write(
                requests=changes,
                session=self._session,
            )

    def _writer_to_document(self, writer: Writer) -> dict[str, Any]:
        document = {
            "id": writer.id.hex,
            "movie_id": writer.movie_id.hex,
            "person_id": writer.person_id.hex,
            "writing": writer.writing,
        }
        return document

    def _pipeline_to_update_writer(
        self,
        clean: Writer,
        dirty: Writer,
    ) -> dict[str, Any]:
        pipeline = {"$set": {}}

        if clean.writing != dirty.writing:
            pipeline["$set"]["writing"] = dirty.writing

        return pipeline
