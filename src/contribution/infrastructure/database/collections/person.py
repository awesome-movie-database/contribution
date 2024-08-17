from typing import NewType

from motor.motor_asyncio import (
    AsyncIOMotorDatabase,
    AsyncIOMotorCollection,
)
from pymongo import IndexModel


async def person_collection_factory(
    database: AsyncIOMotorDatabase,
) -> "PersonCollection":
    collection = database.get_collection("persons")
    await collection.create_indexes([IndexModel(["id"], unique=True)])
    return PersonCollection(collection)


PersonCollection = NewType("PersonCollection", AsyncIOMotorCollection)
