from datetime import date, datetime
from typing import Any, Optional
from decimal import Decimal
from uuid import UUID

from contribution.domain import (
    ContributionStatus,
    Genre,
    MPAA,
    Writing,
    CrewMembership,
    AddMovieContributionId,
    PersonId,
    UserId,
    ContributionRole,
    ContributionWriter,
    ContributionCrewMember,
    PhotoUrl,
    Money,
    AddMovieContribution,
)
from contribution.infrastructure.database.collections import (
    AddMovieContributionCollection,
)
from contribution.infrastructure.database.identity_maps import (
    AddMovieContributionMap,
)
from contribution.infrastructure.database.lock_factory import (
    MongoDBLockFactory,
)
from contribution.infrastructure.database.unit_of_work import (
    MongoDBUnitOfWork,
)


class AddMovieContributionMapper:
    def __init__(
        self,
        contribution_map: AddMovieContributionMap,
        collection: AddMovieContributionCollection,
        lock_factory: MongoDBLockFactory,
        unit_of_work: MongoDBUnitOfWork,
    ):
        self._contribution_map = contribution_map
        self._collection = collection
        self._lock_factory = lock_factory
        self._unit_of_work = unit_of_work

    async def acquire_by_id(
        self,
        id: AddMovieContributionId,
    ) -> Optional[AddMovieContribution]:
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

    async def save(self, contribution: AddMovieContribution) -> None:
        self._contribution_map.save(contribution)
        self._unit_of_work.register_new(contribution)

    async def update(self, contribution: AddMovieContribution) -> None:
        self._unit_of_work.register_dirty(contribution)

    def _document_to_contribution(
        self,
        document: dict[str, Any],
    ) -> AddMovieContribution:
        if document["status_updated_at"]:
            status_updated_at = datetime.fromisoformat(
                document["status_updated_at"],
            )
        else:
            status_updated_at = None

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

        roles = []
        for role_as_dict in document["roles"]:
            role = ContributionRole(
                person_id=PersonId(UUID(role_as_dict["person_id"])),
                character=document["character"],
                importance=document["importance"],
                is_spoiler=document["is_spoiler"],
            )
            roles.append(role)

        writers = []
        for writer_as_dict in document["writers"]:
            writer = ContributionWriter(
                person_id=PersonId(UUID(writer_as_dict["person_id"])),
                writing=Writing(writer_as_dict["writing"]),
            )
            writers.append(writer)

        crew = []
        for crew_member_as_dict in document["crew"]:
            crew_member = ContributionCrewMember(
                person_id=PersonId(UUID(crew_member_as_dict["person_id"])),
                membership=CrewMembership(crew_member_as_dict["membership"]),
            )
            crew.append(crew_member)

        return AddMovieContribution(
            status=ContributionStatus(document["status"]),
            created_at=datetime.fromisoformat(document["created_at"]),
            status_updated_at=status_updated_at,
            id=AddMovieContributionId(UUID(document["id"])),
            author_id=UserId(UUID(document["author_id"])),
            eng_title=document["eng_title"],
            original_title=document["original_title"],
            release_date=date.fromisoformat(document["release_date"]),
            countries=document["countries"],
            genres=[Genre(genre) for genre in document["genres"]],
            mpaa=MPAA(document["mpaa"]),
            duration=document["duration"],
            budget=budget,
            revenue=revenue,
            roles=roles,
            writers=writers,
            crew=crew,
            photos=[PhotoUrl(photo_url) for photo_url in document["photos"]],
        )
