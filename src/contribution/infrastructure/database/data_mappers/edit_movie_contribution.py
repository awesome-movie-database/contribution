from datetime import date, datetime
from typing import Any, Iterable, Mapping, Optional, cast
from decimal import Decimal
from uuid import UUID

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
    ContributionRole,
    ContributionWriter,
    ContributionCrewMember,
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


def genres_factory(genre_values: Iterable[str]) -> list[Genre]:
    return [Genre(genre_value) for genre_value in genre_values]


def budget_factory(budget_as_dict: dict[str, str]) -> Money:
    return Money(
        amount=Decimal(budget_as_dict["amount"]),
        currency=cast(Currency, budget_as_dict["currency"]),
    )


def revenue_factory(revenue_as_dict: dict[str, str]) -> Money:
    return Money(
        amount=Decimal(revenue_as_dict["amount"]),
        currency=cast(Currency, revenue_as_dict["currency"]),
    )


class EditMovieContributionMapper:
    def __init__(
        self,
        contribution_map: EditMovieContributionMap,
        collection: EditMovieContributionCollection,
        lock_factory: MongoDBLockFactory,
        unit_of_work: MongoDBUnitOfWork,
    ):
        self._contribution_map = contribution_map
        self._collection = collection
        self._lock_factory = lock_factory
        self._unit_of_work = unit_of_work

    async def acquire_by_id(
        self,
        id: EditMovieContributionId,
    ) -> Optional[EditMovieContribution]:
        contribution_from_map = self._contribution_map.by_id(id)
        if contribution_from_map and self._contribution_map.is_acquired(
            contribution_from_map,
        ):
            return contribution_from_map

        document = await self._collection.find_one_and_update(
            {"id": id.hex},
            {"$set": {"lock": self._lock_factory()}},
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
            value_factory=genres_factory,
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
            value_factory=budget_factory,
        )
        maybe_revenue = Maybe[Optional[Money]].from_mapping_by_key(
            mapping=document,
            key="revenue",
            value_factory=revenue_factory,
        )

        add_roles = []
        for role_as_dict in document["add_roles"]:
            role = ContributionRole(
                person_id=PersonId(UUID(role_as_dict["person_id"])),
                character=document["character"],
                importance=document["importance"],
                is_spoiler=document["is_spoiler"],
            )
            add_roles.append(role)

        add_writers = []
        for writer_as_dict in document["writers"]:
            writer = ContributionWriter(
                person_id=PersonId(UUID(writer_as_dict["person_id"])),
                writing=Writing(writer_as_dict["writing"]),
            )
            add_writers.append(writer)

        add_crew = []
        for crew_member_as_dict in document["crew"]:
            crew_member = ContributionCrewMember(
                person_id=PersonId(UUID(crew_member_as_dict["person_id"])),
                membership=CrewMembership(crew_member_as_dict["membership"]),
            )
            add_crew.append(crew_member)

        return EditMovieContribution(
            status=ContributionStatus(document["status"]),
            created_at=datetime.fromisoformat(document["created_at"]),
            status_updated_at=status_updated_at,
            id=EditMovieContributionId(UUID(document["id"])),
            author_id=UserId(UUID(document["author_id"])),
            movie_id=MovieId(UUID(document["movie_id"])),
            eng_title=maybe_eng_title,
            original_title=maybe_original_title,
            release_date=maybe_release_date,
            countries=maybe_countries,
            genres=maybe_genres,
            mpaa=maybe_mpaa,
            duration=maybe_duration,
            budget=maybe_budget,
            revenue=maybe_revenue,
            add_roles=add_roles,
            remove_roles=[
                RoleId(UUID(role_id)) for role_id in document["remove_roles"]
            ],
            add_writers=add_writers,
            remove_writers=[
                WriterId(UUID(writer_id))
                for writer_id in document["remove_writers"]
            ],
            add_crew=add_crew,
            remove_crew=[
                CrewMemberId(UUID(crew_member_id))
                for crew_member_id in document["remove_crew"]
            ],
            add_photos=[
                PhotoUrl(photo_url) for photo_url in document["photos"]
            ],
        )
