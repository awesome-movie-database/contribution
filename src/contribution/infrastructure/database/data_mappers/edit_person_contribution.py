from datetime import date, datetime
from typing import Any, Mapping, Optional
from uuid import UUID

from contribution.domain import (
    ContributionStatus,
    Sex,
    EditPersonContributionId,
    UserId,
    PersonId,
    PhotoUrl,
    EditPersonContribution,
    Maybe,
)
from contribution.infrastructure.database.collections import (
    EditPersonContributionCollection,
)
from contribution.infrastructure.database.identity_maps import (
    EditPersonContributionMap,
)
from contribution.infrastructure.database.lock_factory import (
    MongoDBLockFactory,
)
from contribution.infrastructure.database.unit_of_work import (
    MongoDBUnitOfWork,
)


class EditPersonContributionMapper:
    def __init__(
        self,
        contribution_map: EditPersonContributionMap,
        contribution_collection: EditPersonContributionCollection,
        lock_factory: MongoDBLockFactory,
        unit_of_work: MongoDBUnitOfWork,
    ):
        self._contribution_map = contribution_map
        self._contribution_collection = contribution_collection
        self._lock_factory = lock_factory
        self._unit_of_work = unit_of_work

    async def acquire_by_id(
        self,
        id: EditPersonContributionId,
    ) -> Optional[EditPersonContribution]:
        contribution_from_map = self._contribution_map.by_id(id)
        if contribution_from_map and self._contribution_map.is_acquired(
            contribution_from_map,
        ):
            return contribution_from_map

        document = await self._contribution_collection.find_one_and_update(
            {"id": id.hex},
            {"$set": {"lock": self._lock_factory()}},
        )
        if document:
            contribution = self._document_to_contribution(document)
            self._contribution_map.save_acquired(contribution)
            self._unit_of_work.register_clean(contribution)
            return contribution

        return None

    async def save(self, contribution: EditPersonContribution) -> None:
        self._contribution_map.save(contribution)
        self._unit_of_work.register_new(contribution)

    async def update(self, contribution: EditPersonContribution) -> None:
        self._unit_of_work.register_dirty(contribution)

    def _document_to_contribution(
        self,
        document: Mapping[str, Any],
    ) -> EditPersonContribution:
        if document["status_updated_at"]:
            status_updated_at = datetime.fromisoformat(
                document["status_updated_at"],
            )
        else:
            status_updated_at = None

        maybe_first_name = Maybe[str].from_mapping_by_key(
            mapping=document,
            key="first_name",
        )
        maybe_last_name = Maybe[str].from_mapping_by_key(
            mapping=document,
            key="last_name",
        )
        maybe_sex = Maybe[Sex].from_mapping_by_key(
            mapping=document,
            key="sex",
            value_factory=Sex,
        )
        maybe_birth_date = Maybe[date].from_mapping_by_key(
            mapping=document,
            key="birth_date",
            value_factory=date.fromisoformat,
        )
        maybe_death_date = Maybe[date].from_mapping_by_key(
            mapping=document,
            key="death_date",
            value_factory=self._death_date_factory,
        )

        return EditPersonContribution(
            status=ContributionStatus(document["status"]),
            created_at=datetime.fromisoformat(document["created_at"]),
            status_updated_at=status_updated_at,
            id=EditPersonContributionId(UUID(document["id"])),
            author_id=UserId(UUID(document["author_id"])),
            person_id=PersonId(UUID(document["person_id"])),
            first_name=maybe_first_name,
            last_name=maybe_last_name,
            sex=maybe_sex,
            birth_date=maybe_birth_date,
            death_date=maybe_death_date,
            add_photos=[
                PhotoUrl(photo_url) for photo_url in document["photos"]
            ],
        )

    def _death_date_factory(
        self,
        date_string: Optional[str],
    ) -> Optional[date]:
        if date_string:
            return date.fromisoformat(date_string)
        return None
