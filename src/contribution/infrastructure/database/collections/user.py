from typing import NewType

from motor.motor_asyncio import (
    AsyncIOMotorDatabase,
    AsyncIOMotorCollection,
)


def user_collection_factory(
    database: AsyncIOMotorDatabase,
) -> "UserCollection":
    collection = database.get_collection("users")
    return UserCollection(collection)


UserCollection = NewType("UserCollection", AsyncIOMotorCollection)
