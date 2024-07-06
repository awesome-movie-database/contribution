# mypy: disable-error-code="assignment"

from typing import Any, Sequence

from pymongo import InsertOne, UpdateOne, DeleteOne
from motor.motor_asyncio import AsyncIOMotorClientSession

from contribution.domain import Person
from contribution.infrastructure.database.collections import (
    PersonCollection,
)


class CommitPersonCollectionChanges:
    def __init__(
        self,
        collection: PersonCollection,
        session: AsyncIOMotorClientSession,
    ):
        self._collection = collection
        self._session = session

    async def __call__(
        self,
        *,
        new: Sequence[Person],
        clean: Sequence[Person],
        dirty: Sequence[Person],
        deleted: Sequence[Person],
    ) -> None:
        inserts = [
            InsertOne(self._person_to_document(person)) for person in new
        ]
        updates = [
            UpdateOne(
                {"id": clean_person.id},
                self._pipeline_to_update_person(clean_person, dirty_person),
            )
            for clean_person, dirty_person in zip(clean, dirty)
        ]
        deletes = [DeleteOne({"id": person.id}) for person in deleted]

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

    def _person_to_document(self, person: Person) -> dict[str, Any]:
        document = {
            "id": person.id.hex,
            "first_name": person.first_name,
            "last_name": person.last_name,
            "sex": person.sex,
            "birth_date": person.birth_date.isoformat(),
        }

        if person.death_date:
            document["death_date"] = person.death_date.isoformat()
        else:
            document["death_date"] = None

        return document

    def _pipeline_to_update_person(
        self,
        clean: Person,
        dirty: Person,
    ) -> dict[str, Any]:
        pipeline = {"$set": {}}

        if clean.first_name != dirty.first_name:
            pipeline["$set"]["first_name"] = dirty.first_name
        if clean.last_name != dirty.last_name:
            pipeline["$set"]["last_name"] = dirty.last_name
        if clean.sex != dirty.sex:
            pipeline["$set"]["sex"] = dirty.sex
        if clean.birth_date != dirty.birth_date:
            pipeline["$set"]["birth_date"] = dirty.birth_date.isoformat()
        if clean.death_date != dirty.death_date:
            if dirty.death_date:
                pipeline["$set"]["death_date"] = dirty.death_date.isoformat()
            else:
                pipeline["$set"]["death_date"] = None

        return pipeline
