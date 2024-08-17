from typing import NewType

from motor.motor_asyncio import (
    AsyncIOMotorDatabase,
    AsyncIOMotorCollection,
)
from pymongo import IndexModel


async def movie_collection_factory(
    database: AsyncIOMotorDatabase,
) -> "MovieCollection":
    collection = database.get_collection("movies")
    await collection.create_indexes([IndexModel(["id"], unique=True)])
    return MovieCollection(collection)


MovieCollection = NewType("MovieCollection", AsyncIOMotorCollection)
