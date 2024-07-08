from typing import NewType

from motor.motor_asyncio import (
    AsyncIOMotorDatabase,
    AsyncIOMotorCollection,
)


def edit_person_contribution_collection_factory(
    database: AsyncIOMotorDatabase,
) -> "EditPersonContributionCollection":
    collection = database.get_collection("edit_person_contributions")
    return EditPersonContributionCollection(collection)


EditPersonContributionCollection = NewType(
    "EditPersonContributionCollection",
    AsyncIOMotorCollection,
)
