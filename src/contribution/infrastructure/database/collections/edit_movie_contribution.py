from typing import NewType

from motor.motor_asyncio import (
    AsyncIOMotorDatabase,
    AsyncIOMotorCollection,
)


def edit_movie_contribution_collection_factory(
    database: AsyncIOMotorDatabase,
) -> "EditMovieContributionCollection":
    collection = database.get_collection("edit_movie_contributions")
    return EditMovieContributionCollection(collection)


EditMovieContributionCollection = NewType(
    "EditMovieContributionCollection",
    AsyncIOMotorCollection,
)
