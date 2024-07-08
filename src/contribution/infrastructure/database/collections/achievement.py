from typing import NewType

from motor.motor_asyncio import (
    AsyncIOMotorDatabase,
    AsyncIOMotorCollection,
)


def achievement_collection_factory(
    database: AsyncIOMotorDatabase,
) -> "AchievementCollection":
    collection = database.get_collection("achievements")
    return AchievementCollection(collection)


AchievementCollection = NewType(
    "AchievementCollection",
    AsyncIOMotorCollection,
)
