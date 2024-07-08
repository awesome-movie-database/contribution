from typing import NewType

from motor.motor_asyncio import (
    AsyncIOMotorDatabase,
    AsyncIOMotorCollection,
)


def add_person_contribution_collection_factory(
    database: AsyncIOMotorDatabase,
) -> "AddPersonContributionCollection":
    collection = database.get_collection("add_person_contributions")
    return AddPersonContributionCollection(collection)


AddPersonContributionCollection = NewType(
    "AddPersonContributionCollection",
    AsyncIOMotorCollection,
)
