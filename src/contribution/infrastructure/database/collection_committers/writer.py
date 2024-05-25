from typing import Any, Sequence

from motor.motor_asyncio import AsyncIOMotorCollection
from pymongo import InsertOne, UpdateOne, DeleteOne

from contribution.domain import Writer


class CommitWriterCollectionChanges:
    def __init__(self, user_collection: AsyncIOMotorCollection):
        self._collection = user_collection

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

        changes = [*inserts, *updates, *deletes]
        await self._collection.bulk_write(changes)

    def _writer_to_document(self, writer: Writer) -> dict[str, Any]:
        document = {
            "id": writer.id.hex,
            "movie_id": writer.movie_id.hex,
            "person_id": writer.person_id.hex,
            "writing": writer.writing.value,
        }
        return document

    def _pipeline_to_update_writer(
        self,
        clean: Writer,
        dirty: Writer,
    ) -> dict[str, Any]:
        pipeline = {"$set": {}}

        if clean.writing != dirty.writing:
            pipeline["$set"]["writing"] = dirty.writing.value

        return pipeline
