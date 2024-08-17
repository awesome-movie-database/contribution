from typing import NewType

from motor.motor_asyncio import (
    AsyncIOMotorDatabase,
    AsyncIOMotorCollection,
)
from pymongo import IndexModel


async def crew_member_collection_factory(
    database: AsyncIOMotorDatabase,
) -> "CrewMemberCollection":
    collection = database.get_collection("crew_members")
    await collection.create_indexes([IndexModel(["id"], unique=True)])
    return CrewMemberCollection(collection)


CrewMemberCollection = NewType(
    "CrewMemberCollection",
    AsyncIOMotorCollection,
)
