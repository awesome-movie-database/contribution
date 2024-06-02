from datetime import date, datetime
from typing import Any, Optional
from uuid import UUID

from contribution.domain import (
    ContributionStatus,
    Sex,
    AddPersonContributionId,
    UserId,
    PhotoUrl,
    AddPersonContribution,
)
from contribution.infrastructure.database.collections import (
    AddPersonContributionCollection,
)
from contribution.infrastructure.database.identity_maps import (
    AddPersonContributionMap,
)
from contribution.infrastructure.database.lock_factory import (
    MongoDBLockFactory,
)
from contribution.infrastructure.database.unit_of_work import (
    MongoDBUnitOfWork,
)


class AddPersonContributionMapper:
    def __init__(
        self,
        contribution_map: AddPersonContributionMap,
        collection: AddPersonContributionCollection,
        lock_factory: MongoDBLockFactory,
        unit_of_work: MongoDBUnitOfWork,
    ):
        self._contribution_map = contribution_map
        self._collection = collection
        self._lock_factory = lock_factory
        self._unit_of_work = unit_of_work

    async def acquire_by_id(
        self,
        id: AddPersonContributionId,
    ) -> Optional[AddPersonContribution]:
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

    async def save(self, contribution: AddPersonContribution) -> None:
        self._contribution_map.save(contribution)
        self._unit_of_work.register_new(contribution)

    async def update(self, contribution: AddPersonContribution) -> None:
        self._unit_of_work.register_dirty(contribution)

    def _document_to_contribution(
        self,
        document: dict[str, Any],
    ) -> AddPersonContribution:
        if document["status_updated_at"]:
            status_updated_at = datetime.fromisoformat(
                document["status_updated_at"],
            )
        else:
            status_updated_at = None

        if document["death_date"]:
            death_date = date.fromisoformat(document["death_date"])
        else:
            death_date = None

        return AddPersonContribution(
            status=ContributionStatus(document["status"]),
            created_at=datetime.fromisoformat(document["created_at"]),
            status_updated_at=status_updated_at,
            id=AddPersonContributionId(UUID(document["id"])),
            author_id=UserId(UUID(document["author_id"])),
            first_name=document["first_name"],
            last_name=document["last_name"],
            sex=Sex(document["sex"]),
            birth_date=date.fromisoformat(document["birth_date"]),
            death_date=death_date,
            photos=[PhotoUrl(photo_url) for photo_url in document["photos"]],
        )
