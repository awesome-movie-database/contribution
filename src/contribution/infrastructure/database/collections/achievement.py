from typing import NewType

from motor.motor_asyncio import (
    AsyncIOMotorDatabase,
    AsyncIOMotorCollection,
)
from pymongo import IndexModel


async def achievement_collection_factory(
    database: AsyncIOMotorDatabase,
) -> "AchievementCollection":
    collection = database.get_collection("achievements")
    await collection.create_indexes(
        [
            IndexModel(["id"], unique=True),
            IndexModel(["user_id", "achieved"], unique=True),
        ],
    )
    return AchievementCollection(collection)


AchievementCollection = NewType(
    "AchievementCollection",
    AsyncIOMotorCollection,
)
