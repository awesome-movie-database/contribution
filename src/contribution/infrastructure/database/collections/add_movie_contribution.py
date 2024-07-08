from typing import NewType

from motor.motor_asyncio import (
    AsyncIOMotorDatabase,
    AsyncIOMotorCollection,
)


def add_movie_contribution_collection_factory(
    database: AsyncIOMotorDatabase,
) -> "AddMovieContributionCollection":
    collection = database.get_collection("add_movie_contributions")
    return AddMovieContributionCollection(collection)


AddMovieContributionCollection = NewType(
    "AddMovieContributionCollection",
    AsyncIOMotorCollection,
)
