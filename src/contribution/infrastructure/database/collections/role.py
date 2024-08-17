from typing import NewType

from motor.motor_asyncio import (
    AsyncIOMotorDatabase,
    AsyncIOMotorCollection,
)
from pymongo import IndexModel


async def role_collection_factory(
    database: AsyncIOMotorDatabase,
) -> "RoleCollection":
    collection = database.get_collection("roles")
    await collection.create_indexes(
        [
            IndexModel(["id"], unique=True),
            IndexModel(["character", "person_id"], unique=True),
        ],
    )
    return RoleCollection(collection)


RoleCollection = NewType("RoleCollection", AsyncIOMotorCollection)
