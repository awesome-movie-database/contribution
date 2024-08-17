from typing import NewType

from motor.motor_asyncio import (
    AsyncIOMotorDatabase,
    AsyncIOMotorCollection,
)
from pymongo import IndexModel


async def writer_collection_factory(
    database: AsyncIOMotorDatabase,
) -> "WriterCollection":
    collection = database.get_collection("writers")
    await collection.create_indexes(
        [
            IndexModel(["id"], unique=True),
            IndexModel(["person_id", "movie_id", "writing"], unique=True),
        ],
    )
    return WriterCollection(collection)


WriterCollection = NewType("WriterCollection", AsyncIOMotorCollection)
