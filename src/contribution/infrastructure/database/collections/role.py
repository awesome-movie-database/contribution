from typing import NewType

from motor.motor_asyncio import (
    AsyncIOMotorDatabase,
    AsyncIOMotorCollection,
)


def role_collection_factory(
    database: AsyncIOMotorDatabase,
) -> "RoleCollection":
    collection = database.get_collection("roles")
    return RoleCollection(collection)


RoleCollection = NewType("RoleCollection", AsyncIOMotorCollection)
