# mypy: disable-error-code="assignment"

from typing import Any, Sequence

from pymongo import InsertOne, UpdateOne, DeleteOne
from motor.motor_asyncio import AsyncIOMotorClientSession

from contribution.domain import EditPersonContribution
from contribution.infrastructure.database.collections import (
    EditPersonContributionCollection,
)


class CommitEditPersonContributionCollectionChanges:
    def __init__(
        self,
        collection: EditPersonContributionCollection,
        session: AsyncIOMotorClientSession,
    ):
        self._collection = collection
        self._session = session

    async def __call__(
        self,
        *,
        new: Sequence[EditPersonContribution],
        clean: Sequence[EditPersonContribution],
        dirty: Sequence[EditPersonContribution],
        deleted: Sequence[EditPersonContribution],
    ) -> None:
        inserts = [
            InsertOne(self._contribution_to_document(contribution))
            for contribution in new
        ]
        updates = [
            UpdateOne(
                {"id": clean_contribution.id},
                self._pipeline_to_update_contribution(
                    clean_contribution,
                    dirty_contribution,
                ),
            )
            for clean_contribution, dirty_contribution in zip(clean, dirty)
        ]
        deletes = [
            DeleteOne({"id": contribution.id}) for contribution in deleted
        ]

        changes: list[InsertOne, UpdateOne, DeleteOne] = [
            *inserts,
            *updates,
            *deletes,
        ]
        if changes:
            await self._collection.bulk_write(
                requests=changes,
                session=self._session,
            )

    def _contribution_to_document(
        self,
        contribution: EditPersonContribution,
    ) -> dict[str, Any]:
        document = {
            "id": contribution.id.hex,
            "status": contribution.status,
            "author_id": contribution.author_id.hex,
            "person_id": contribution.person_id.hex,
            "photos_to_add": list(contribution.photos_to_add),
        }

        if contribution.status_updated_at:
            document[
                "status_updated_at"
            ] = contribution.status_updated_at.isoformat()
        else:
            document["status_updated_at"] = None
        if contribution.first_name.is_set:
            document["first_name"] = contribution.first_name.value
        if contribution.last_name.is_set:
            document["last_name"] = contribution.last_name.value
        if contribution.sex.is_set:
            document["sex"] = contribution.sex.value
        if contribution.birth_date.is_set:
            document["birth_date"] = contribution.birth_date.value.isoformat()
        if contribution.death_date.is_set:
            death_date = contribution.death_date.value
            if death_date:
                document["death_date"] = death_date.isoformat()
            else:
                document["death_date"] = None

        return document

    def _pipeline_to_update_contribution(
        self,
        clean: EditPersonContribution,
        dirty: EditPersonContribution,
    ) -> dict[str, Any]:
        pipeline = {"$set": {}, "$unset": {}}

        if clean.status != dirty.status:
            pipeline["$set"]["status"] = dirty.status
        if clean.status_updated_at != dirty.status_updated_at:
            if dirty.status_updated_at:
                pipeline["$set"][
                    "status_updated_at"
                ] = dirty.status_updated_at.isoformat()
            else:
                pipeline["$set"]["status_updated_at"] = None
        if clean.first_name != dirty.first_name:
            if dirty.first_name.is_set:
                pipeline["$set"]["first_name"] = dirty.first_name.value
            else:
                pipeline["$unset"]["first_name"] = ""
        if clean.last_name != dirty.last_name:
            if dirty.last_name.is_set:
                pipeline["$set"]["last_name"] = dirty.last_name.value
            else:
                pipeline["$unset"]["last_name"] = ""
        if clean.sex != dirty.sex:
            if dirty.sex.is_set:
                pipeline["$set"]["sex"] = dirty.sex.value
            else:
                pipeline["$unset"]["sex"] = ""
        if clean.birth_date != dirty.birth_date:
            if dirty.birth_date.is_set:
                pipeline["$set"][
                    "birth_date"
                ] = dirty.birth_date.value.isoformat()
            else:
                pipeline["$unset"]["birth_date"] = ""
        if clean.death_date != dirty.death_date:
            if dirty.death_date.is_set:
                death_date = dirty.death_date.value
                if death_date:
                    pipeline["$set"]["death_date"] = death_date.isoformat()
                else:
                    pipeline["$set"]["death_date"] = None
            else:
                pipeline["$unset"]["death_date"] = ""
        if clean.photos_to_add != dirty.photos_to_add:
            pipeline["$set"]["photos_to_add"] = list(dirty.photos_to_add)

        return pipeline
