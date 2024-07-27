from typing import NewType

from motor.motor_asyncio import (
    AsyncIOMotorDatabase,
    AsyncIOMotorCollection,
)
from pymongo import IndexModel


async def user_collection_factory(
    database: AsyncIOMotorDatabase,
) -> "UserCollection":
    collection = database.get_collection("users")
    await collection.create_indexes(
        [IndexModel(["id", "name", "email"], unique=True)],
    )
    return UserCollection(collection)


UserCollection = NewType("UserCollection", AsyncIOMotorCollection)
