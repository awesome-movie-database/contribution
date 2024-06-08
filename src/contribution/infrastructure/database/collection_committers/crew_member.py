from typing import Any, Sequence

from pymongo import InsertOne, UpdateOne, DeleteOne

from contribution.domain import CrewMember
from contribution.infrastructure.database.collections import (
    CrewMemberCollection,
)


class CommitCrewMemberCollectionChanges:
    def __init__(self, collection: CrewMemberCollection):
        self._collection = collection

    async def __call__(
        self,
        *,
        new: Sequence[CrewMember],
        clean: Sequence[CrewMember],
        dirty: Sequence[CrewMember],
        deleted: Sequence[CrewMember],
    ) -> None:
        inserts = [
            InsertOne(self._crew_member_to_document(crew_member))
            for crew_member in new
        ]
        updates = [
            UpdateOne(
                {"id": clean_crew_member.id},
                self._pipeline_to_update_crew_member(
                    clean_crew_member,
                    dirty_crew_member,
                ),
            )
            for clean_crew_member, dirty_crew_member in zip(clean, dirty)
        ]
        deletes = [
            DeleteOne({"id": crew_member.id}) for crew_member in deleted
        ]

        changes = [*inserts, *updates, *deletes]
        await self._collection.bulk_write(changes)

    def _crew_member_to_document(
        self,
        crew_member: CrewMember,
    ) -> dict[str, Any]:
        document = {
            "id": crew_member.id.hex,
            "movie_id": crew_member.movie_id.hex,
            "person_id": crew_member.person_id.hex,
            "membership": crew_member.membership,
        }
        return document

    def _pipeline_to_update_crew_member(
        self,
        clean: CrewMember,
        dirty: CrewMember,
    ) -> dict[str, Any]:
        pipeline = {"$set": {}}

        if clean.membership != dirty.membership:
            pipeline["$set"]["membership"] = dirty.membership

        return pipeline
