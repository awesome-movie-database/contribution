from typing import NewType

from motor.motor_asyncio import (
    AsyncIOMotorDatabase,
    AsyncIOMotorCollection,
)
from pymongo import IndexModel


async def add_movie_contribution_collection_factory(
    database: AsyncIOMotorDatabase,
) -> "AddMovieContributionCollection":
    collection = database.get_collection("add_movie_contributions")
    await collection.create_indexes([IndexModel(["id"], unique=True)])
    return AddMovieContributionCollection(collection)


AddMovieContributionCollection = NewType(
    "AddMovieContributionCollection",
    AsyncIOMotorCollection,
)
