from typing import NewType

from motor.motor_asyncio import (
    AsyncIOMotorDatabase,
    AsyncIOMotorCollection,
)


def crew_member_collection_factory(
    database: AsyncIOMotorDatabase,
) -> "CrewMemberCollection":
    collection = database.get_collection("crew_members")
    return CrewMemberCollection(collection)


CrewMemberCollection = NewType(
    "CrewMemberCollection",
    AsyncIOMotorCollection,
)
