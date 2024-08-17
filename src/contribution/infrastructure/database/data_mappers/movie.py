from typing import Any, Mapping, Optional
from decimal import Decimal
from datetime import date
from uuid import UUID

from motor.motor_asyncio import AsyncIOMotorClientSession

from contribution.domain import (
    Genre,
    MPAA,
    MovieId,
    Money,
    Movie,
)
from contribution.infrastructure.database.collections import (
    MovieCollection,
)
from contribution.infrastructure.database.identity_maps import (
    MovieMap,
)
from contribution.infrastructure.database.lock_factory import (
    MongoDBLockFactory,
)
from contribution.infrastructure.database.unit_of_work import (
    MongoDBUnitOfWork,
)


class MovieMapper:
    def __init__(
        self,
        movie_map: MovieMap,
        movie_collection: MovieCollection,
        lock_factory: MongoDBLockFactory,
        unit_of_work: MongoDBUnitOfWork,
        session: AsyncIOMotorClientSession,
    ):
        self._movie_map = movie_map
        self._movie_collection = movie_collection
        self._lock_factory = lock_factory
        self._unit_of_work = unit_of_work
        self._session = session

    async def by_id(self, id: MovieId) -> Optional[Movie]:
        movie_from_map = self._movie_map.by_id(id)
        if movie_from_map:
            return movie_from_map

        document = await self._movie_collection.find_one(
            {"id": id.hex},
            session=self._session,
        )
        if document:
            movie = self._document_to_movie(document)
            self._movie_map.save(movie)
            self._unit_of_work.register_clean(movie)
            return movie

        return None

    async def acquire_by_id(self, id: MovieId) -> Optional[Movie]:
        movie_from_map = self._movie_map.by_id(id)
        if movie_from_map and self._movie_map.is_acquired(movie_from_map):
            return movie_from_map

        document = await self._movie_collection.find_one_and_update(
            {"id": id.hex},
            {"$set": {"lock": self._lock_factory()}},
            session=self._session,
        )
        if document:
            movie = self._document_to_movie(document)
            self._movie_map.save_acquired(movie)
            self._unit_of_work.register_clean(movie)
            return movie

        return None

    async def save(self, movie: Movie) -> None:
        self._movie_map.save(movie)
        self._unit_of_work.register_new(movie)

    async def update(self, movie: Movie) -> None:
        self._unit_of_work.register_dirty(movie)

    def _document_to_movie(self, document: Mapping[str, Any]) -> Movie:
        budget_as_dict = document["budget"]
        if budget_as_dict:
            budget = Money(
                amount=Decimal(budget_as_dict["amount"]),
                currency=budget_as_dict["currency"],
            )
        else:
            budget = None

        revenue_as_dict = document["revenue"]
        if revenue_as_dict:
            revenue = Money(
                amount=Decimal(revenue_as_dict["amount"]),
                currency=revenue_as_dict["currency"],
            )
        else:
            revenue = None

        return Movie(
            id=MovieId(UUID(document["id"])),
            eng_title=document["eng_title"],
            original_title=document["original_title"],
            summary=document["summary"],
            description=document["description"],
            release_date=date.fromisoformat(document["release_date"]),
            countries=document["countries"],
            genres=[Genre(genre) for genre in document["genres"]],
            mpaa=MPAA(document["mpaa"]),
            duration=document["duration"],
            budget=budget,
            revenue=revenue,
        )
