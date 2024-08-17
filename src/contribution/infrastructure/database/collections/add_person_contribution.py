from typing import NewType

from motor.motor_asyncio import (
    AsyncIOMotorDatabase,
    AsyncIOMotorCollection,
)
from pymongo import IndexModel


async def add_person_contribution_collection_factory(
    database: AsyncIOMotorDatabase,
) -> "AddPersonContributionCollection":
    collection = database.get_collection("add_person_contributions")
    await collection.create_indexes([IndexModel(["id"], unique=True)])
    return AddPersonContributionCollection(collection)


AddPersonContributionCollection = NewType(
    "AddPersonContributionCollection",
    AsyncIOMotorCollection,
)
