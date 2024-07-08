from typing import NewType

from motor.motor_asyncio import (
    AsyncIOMotorDatabase,
    AsyncIOMotorCollection,
)


def person_collection_factory(
    database: AsyncIOMotorDatabase,
) -> "PersonCollection":
    collection = database.get_collection("persons")
    return PersonCollection(collection)


PersonCollection = NewType("PersonCollection", AsyncIOMotorCollection)
