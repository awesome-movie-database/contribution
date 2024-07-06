from typing import Any, Sequence

from pymongo import InsertOne, UpdateOne, DeleteOne
from motor.motor_asyncio import AsyncIOMotorClientSession

from contribution.domain import Movie
from contribution.infrastructure.database.collections import (
    MovieCollection,
)


class CommitMovieCollectionChanges:
    def __init__(
        self,
        collection: MovieCollection,
        session: AsyncIOMotorClientSession,
    ):
        self._collection = collection
        self._session = session

    async def __call__(
        self,
        *,
        new: Sequence[Movie],
        clean: Sequence[Movie],
        dirty: Sequence[Movie],
        deleted: Sequence[Movie],
    ) -> None:
        inserts = [InsertOne(self._movie_to_document(movie)) for movie in new]
        updates = [
            UpdateOne(
                {"id": clean_movie.id},
                self._pipeline_to_update_movie(clean_movie, dirty_movie),
            )
            for clean_movie, dirty_movie in zip(clean, dirty)
        ]
        deletes = [DeleteOne({"id": movie.id}) for movie in deleted]

        changes: list[InsertOne, UpdateOne, DeleteOne] = [
            *inserts,
            *updates,
            *deletes,
        ]
        await self._collection.bulk_write(
            requests=changes,
            session=self._session,
        )

    def _movie_to_document(self, movie: Movie) -> dict[str, Any]:
        document = {
            "id": movie.id.hex,
            "eng_title": movie.eng_title,
            "original_title": movie.original_title,
            "release_date": movie.release_date.isoformat(),
            "countries": list(movie.countries),
            "genres": list(movie.genres),
            "mpaa": movie.mpaa,
            "duration": movie.duration,
        }

        if movie.budget:
            document["budget"] = {
                "amount": movie.budget.amount,
                "currency": movie.budget.currency,
            }
        else:
            document["budget"] = None

        if movie.revenue:
            document["revenue"] = {
                "amount": movie.revenue.amount,
                "currency": movie.revenue.currency,
            }
        else:
            document["revenue"] = None

        return document

    def _pipeline_to_update_movie(
        self,
        clean: Movie,
        dirty: Movie,
    ) -> dict[str, Any]:
        pipeline = {"$set": {}}

        if clean.eng_title != dirty.eng_title:
            pipeline["$set"]["eng_title"] = dirty.eng_title
        if clean.original_title != dirty.original_title:
            pipeline["$set"]["original_title"] = dirty.original_title
        if clean.release_date != dirty.release_date:
            pipeline["$set"]["release_date"] = dirty.release_date.isoformat()
        if clean.countries != dirty.countries:
            pipeline["$set"]["countries"] = list(dirty.countries)
        if clean.genres != dirty.genres:
            pipeline["$set"]["genres"] = list(dirty.genres)
        if clean.mpaa != dirty.mpaa:
            pipeline["$set"]["mpaa"] = dirty.mpaa
        if clean.duration != dirty.duration:
            pipeline["$set"]["duration"] = dirty.duration
        if clean.budget != dirty.budget:
            if dirty.budget:
                pipeline["$set"]["budget"] = {
                    "amount": str(dirty.budget.amount),
                    "currency": dirty.budget.currency,
                }
            else:
                pipeline["$set"]["budget"] = None
        if clean.revenue != dirty.revenue:
            if dirty.revenue:
                pipeline["$set"]["revenue"] = {
                    "amount": str(dirty.revenue.amount),
                    "currency": dirty.revenue.currency,
                }
            else:
                pipeline["$set"]["revenue"] = None

        return pipeline
