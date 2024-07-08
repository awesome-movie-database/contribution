from typing import NewType

from motor.motor_asyncio import (
    AsyncIOMotorDatabase,
    AsyncIOMotorCollection,
)


def permissions_collection_factory(
    database: AsyncIOMotorDatabase,
) -> "PermissionsCollection":
    collection = database.get_collection("permissions")
    return PermissionsCollection(collection)


PermissionsCollection = NewType(
    "PermissionsCollection",
    AsyncIOMotorCollection,
)
