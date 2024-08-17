from typing import NewType

from motor.motor_asyncio import (
    AsyncIOMotorDatabase,
    AsyncIOMotorCollection,
)
from pymongo import IndexModel


async def edit_movie_contribution_collection_factory(
    database: AsyncIOMotorDatabase,
) -> "EditMovieContributionCollection":
    collection = database.get_collection("edit_movie_contributions")
    await collection.create_indexes([IndexModel(["id"], unique=True)])
    return EditMovieContributionCollection(collection)


EditMovieContributionCollection = NewType(
    "EditMovieContributionCollection",
    AsyncIOMotorCollection,
)
