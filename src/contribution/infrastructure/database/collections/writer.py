from typing import NewType

from motor.motor_asyncio import (
    AsyncIOMotorDatabase,
    AsyncIOMotorCollection,
)


def writer_collection_factory(
    database: AsyncIOMotorDatabase,
) -> "WriterCollection":
    collection = database.get_collection("writers")
    return WriterCollection(collection)


WriterCollection = NewType("WriterCollection", AsyncIOMotorCollection)
