from typing import NewType

from motor.motor_asyncio import (
    AsyncIOMotorDatabase,
    AsyncIOMotorCollection,
)
from pymongo import IndexModel


async def edit_person_contribution_collection_factory(
    database: AsyncIOMotorDatabase,
) -> "EditPersonContributionCollection":
    collection = database.get_collection("edit_person_contributions")
    await collection.create_indexes([IndexModel(["id"], unique=True)])
    return EditPersonContributionCollection(collection)


EditPersonContributionCollection = NewType(
    "EditPersonContributionCollection",
    AsyncIOMotorCollection,
)
