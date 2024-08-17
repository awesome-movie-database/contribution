from datetime import date, datetime
from typing import Any, Iterable, Mapping, Optional, cast
from decimal import Decimal
from uuid import UUID

from motor.motor_asyncio import AsyncIOMotorClientSession

from contribution.domain import (
    ContributionStatus,
    Genre,
    MPAA,
    Writing,
    CrewMembership,
    EditMovieContributionId,
    PersonId,
    MovieId,
    UserId,
    RoleId,
    WriterId,
    CrewMemberId,
    MovieRole,
    MovieWriter,
    MovieCrewMember,
    Country,
    Currency,
    PhotoUrl,
    Money,
    EditMovieContribution,
    Maybe,
)
from contribution.infrastructure.database.collections import (
    EditMovieContributionCollection,
)
from contribution.infrastructure.database.identity_maps import (
    EditMovieContributionMap,
)
from contribution.infrastructure.database.lock_factory import (
    MongoDBLockFactory,
)
from contribution.infrastructure.database.unit_of_work import (
    MongoDBUnitOfWork,
)


class EditMovieContributionMapper:
    def __init__(
        self,
        contribution_map: EditMovieContributionMap,
        contribution_collection: EditMovieContributionCollection,
        lock_factory: MongoDBLockFactory,
        unit_of_work: MongoDBUnitOfWork,
        session: AsyncIOMotorClientSession,
    ):
        self._contribution_map = contribution_map
        self._contribution_collection = contribution_collection
        self._lock_factory = lock_factory
        self._unit_of_work = unit_of_work
        self._session = session

    async def acquire_by_id(
        self,
        id: EditMovieContributionId,
    ) -> Optional[EditMovieContribution]:
        contribution_from_map = self._contribution_map.by_id(id)
        if contribution_from_map and self._contribution_map.is_acquired(
            contribution_from_map,
        ):
            return contribution_from_map

        document = await self._contribution_collection.find_one_and_update(
            {"id": id.hex},
            {"$set": {"lock": self._lock_factory()}},
            session=self._session,
        )
        if document:
            contribution = self._document_to_contribution(document)
            self._contribution_map.save_acquired(contribution)
            self._unit_of_work.register_clean(contribution)
            return contribution

        return None

    async def save(self, contribution: EditMovieContribution) -> None:
        self._contribution_map.save(contribution)
        self._unit_of_work.register_new(contribution)

    async def update(self, contribution: EditMovieContribution) -> None:
        self._unit_of_work.register_dirty(contribution)

    def _document_to_contribution(
        self,
        document: Mapping[str, Any],
    ) -> EditMovieContribution:
        if document["status_updated_at"]:
            status_updated_at = datetime.fromisoformat(
                document["status_updated_at"],
            )
        else:
            status_updated_at = None

        maybe_eng_title = Maybe[str].from_mapping_by_key(
            mapping=document,
            key="eng_title",
        )
        maybe_original_title = Maybe[str].from_mapping_by_key(
            mapping=document,
            key="original_title",
        )
        maybe_summary = Maybe[str].from_mapping_by_key(
            mapping=document,
            key="summary",
        )
        maybe_description = Maybe[str].from_mapping_by_key(
            mapping=document,
            key="duration",
        )
        maybe_release_date = Maybe[date].from_mapping_by_key(
            mapping=document,
            key="release_date",
            value_factory=date.fromisoformat,
        )
        maybe_countries = Maybe[list[Country]].from_mapping_by_key(
            mapping=document,
            key="countries",
        )
        maybe_genres = Maybe[list[Genre]].from_mapping_by_key(
            mapping=document,
            key="genres",
            value_factory=self._genres_factory,
        )
        maybe_mpaa = Maybe[MPAA].from_mapping_by_key(
            mapping=document,
            key="mpaa",
            value_factory=MPAA,
        )
        maybe_duration = Maybe[int].from_mapping_by_key(
            mapping=document,
            key="duration",
        )
        maybe_budget = Maybe[Optional[Money]].from_mapping_by_key(
            mapping=document,
            key="budget",
            value_factory=self._budget_factory,
        )
        maybe_revenue = Maybe[Optional[Money]].from_mapping_by_key(
            mapping=document,
            key="revenue",
            value_factory=self._revenue_factory,
        )

        roles_to_add = []
        for role_as_dict in document["roles_to_add"]:
            role = MovieRole(
                id=RoleId(UUID(role_as_dict["id"])),
                person_id=PersonId(UUID(role_as_dict["person_id"])),
                character=document["character"],
                importance=document["importance"],
                is_spoiler=document["is_spoiler"],
            )
            roles_to_add.append(role)

        writers_to_add = []
        for writer_as_dict in document["writers"]:
            writer = MovieWriter(
                id=WriterId(UUID(writer_as_dict["id"])),
                person_id=PersonId(UUID(writer_as_dict["person_id"])),
                writing=Writing(writer_as_dict["writing"]),
            )
            writers_to_add.append(writer)

        crew_to_add = []
        for crew_member_as_dict in document["crew"]:
            crew_member = MovieCrewMember(
                id=CrewMemberId(UUID(crew_member_as_dict["id"])),
                person_id=PersonId(UUID(crew_member_as_dict["person_id"])),
                membership=CrewMembership(crew_member_as_dict["membership"]),
            )
            crew_to_add.append(crew_member)

        return EditMovieContribution(
            status=ContributionStatus(document["status"]),
            created_at=datetime.fromisoformat(document["created_at"]),
            status_updated_at=status_updated_at,
            id=EditMovieContributionId(UUID(document["id"])),
            author_id=UserId(UUID(document["author_id"])),
            movie_id=MovieId(UUID(document["movie_id"])),
            eng_title=maybe_eng_title,
            original_title=maybe_original_title,
            summary=maybe_summary,
            description=maybe_description,
            release_date=maybe_release_date,
            countries=maybe_countries,
            genres=maybe_genres,
            mpaa=maybe_mpaa,
            duration=maybe_duration,
            budget=maybe_budget,
            revenue=maybe_revenue,
            roles_to_add=roles_to_add,
            roles_to_remove=[
                RoleId(UUID(role_id))
                for role_id in document["roles_to_remove"]
            ],
            writers_to_add=writers_to_add,
            writers_to_remove=[
                WriterId(UUID(writer_id))
                for writer_id in document["writers_to_remove"]
            ],
            crew_to_add=crew_to_add,
            crew_to_remove=[
                CrewMemberId(UUID(crew_member_id))
                for crew_member_id in document["crew_to_remove"]
            ],
            photos_to_add=[
                PhotoUrl(photo_url) for photo_url in document["photos_to_add"]
            ],
        )

    def _genres_factory(self, genre_values: Iterable[str]) -> list[Genre]:
        return [Genre(genre_value) for genre_value in genre_values]

    def _budget_factory(self, budget_as_dict: dict[str, str]) -> Money:
        return Money(
            amount=Decimal(budget_as_dict["amount"]),
            currency=cast(Currency, budget_as_dict["currency"]),
        )

    def _revenue_factory(self, revenue_as_dict: dict[str, str]) -> Money:
        return Money(
            amount=Decimal(revenue_as_dict["amount"]),
            currency=cast(Currency, revenue_as_dict["currency"]),
        )
