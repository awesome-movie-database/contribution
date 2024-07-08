from typing import NewType

from motor.motor_asyncio import (
    AsyncIOMotorDatabase,
    AsyncIOMotorCollection,
)


def movie_collection_factory(
    database: AsyncIOMotorDatabase,
) -> "MovieCollection":
    collection = database.get_collection("movies")
    return MovieCollection(collection)


MovieCollection = NewType("MovieCollection", AsyncIOMotorCollection)
