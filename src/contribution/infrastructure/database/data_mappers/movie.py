from typing import Any, Optional
from decimal import Decimal
from datetime import date
from uuid import UUID

from motor.motor_asyncio import AsyncIOMotorCollection

from contribution.domain import (
    Genre,
    MPAA,
    MovieId,
    Money,
    Movie,
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
        collection: AsyncIOMotorCollection,
        lock_factory: MongoDBLockFactory,
        unit_of_work: MongoDBUnitOfWork,
    ):
        self._movie_map = movie_map
        self._collection = collection
        self._lock_factory = lock_factory
        self._unit_of_work = unit_of_work

    async def by_id(self, id: MovieId) -> Optional[Movie]:
        movie_from_map = self._movie_map.by_id(id)
        if movie_from_map:
            return movie_from_map

        document_or_none = await self._collection.find_one(
            {"id": id.hex},
        )
        if document_or_none:
            movie = self._document_to_movie(document_or_none)
            self._movie_map.save(movie)
            self._unit_of_work.register_clean(movie)
            return movie

        return None

    async def acquire_by_id(self, id: MovieId) -> Optional[Movie]:
        movie_from_map = self._movie_map.by_id(id)
        if movie_from_map and self._movie_map.is_acquired(movie_from_map):
            return movie_from_map

        document_or_none = await self._collection.find_one_and_update(
            {"id": id.hex},
            {"$set": {"lock": self._lock_factory()}},
        )
        if document_or_none:
            movie = self._document_to_movie(document_or_none)
            self._movie_map.save_acquired(movie)
            self._unit_of_work.register_clean(movie)
            return movie

        return None

    async def save(self, movie: Movie) -> None:
        self._movie_map.save(movie)
        self._unit_of_work.register_new(movie)

    async def update(self, movie: Movie) -> None:
        self._unit_of_work.register_dirty(movie)

    def _document_to_movie(self, document: dict[str, Any]) -> Movie:
        budget_or_none = document["budget"]
        if budget_or_none:
            budget = Money(
                amount=Decimal(budget_or_none["amount"]),
                currency=budget_or_none["currency"],
            )
        else:
            budget = None

        revenue_or_none = document["revenue"]
        if revenue_or_none:
            revenue = Money(
                amount=Decimal(revenue_or_none["amount"]),
                currency=revenue_or_none["currency"],
            )
        else:
            revenue = None

        return Movie(
            id=MovieId(UUID(document["id"])),
            eng_title=document["eng_title"],
            original_title=document["original_title"],
            release_date=date.fromisoformat(document["release_date"]),
            countries=document["countries"],
            genres=[Genre(genre) for genre in document["genres"]],
            mpaa=MPAA(document["mpaa"]),
            duration=document["duration"],
            budget=budget,
            revenue=revenue,
        )
