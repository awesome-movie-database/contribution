from typing import Any, Iterable, Mapping, Optional
from datetime import date
from uuid import UUID

from contribution.domain import PersonId, Sex, Person
from contribution.infrastructure.database.collections import (
    PersonCollection,
)
from contribution.infrastructure.database.identity_maps import (
    PersonMap,
)
from contribution.infrastructure.database.lock_factory import (
    MongoDBLockFactory,
)
from contribution.infrastructure.database.unit_of_work import (
    MongoDBUnitOfWork,
)


class PersonMapper:
    def __init__(
        self,
        person_map: PersonMap,
        collection: PersonCollection,
        lock_factory: MongoDBLockFactory,
        unit_of_work: MongoDBUnitOfWork,
    ):
        self._person_map = person_map
        self._collection = collection
        self._lock_factory = lock_factory
        self._unit_of_work = unit_of_work

    async def by_id(self, id: PersonId) -> Optional[Person]:
        person_from_map = self._person_map.by_id(id)
        if person_from_map:
            return person_from_map

        document = await self._collection.find_one({"id": id.hex})
        if document:
            person = self._document_to_person(document)
            self._person_map.save(person)
            self._unit_of_work.register_clean(person)
            return person

        return None

    async def acquire_by_id(self, id: PersonId) -> Optional[Person]:
        person_from_map = self._person_map.by_id(id)
        if person_from_map and self._person_map.is_acquired(person_from_map):
            return person_from_map

        document = await self._collection.find_one_and_update(
            {"id": id.hex},
            {"$set": {"lock": self._lock_factory()}},
        )
        if document:
            person = self._document_to_person(document)
            self._person_map.save_acquired(person)
            self._unit_of_work.register_clean(person)
            return person

        return None

    async def list_by_ids(
        self,
        ids: Iterable[PersonId],
    ) -> list[Person]:
        persons_from_map = []
        for id in ids:
            person_from_map = self._person_map.by_id(id)
            if not person_from_map:
                break
            persons_from_map.append(person_from_map)
        else:
            return persons_from_map

        documents = await self._collection.find(
            {"$in": list(ids)},
        ).to_list(None)

        persons = []
        for document in documents:
            person = self._document_to_person(document)
            self._person_map.save(person)
            self._unit_of_work.register_clean(person)
            persons.append(person)

        return persons

    async def save(self, person: Person) -> None:
        self._person_map.save(person)
        self._unit_of_work.register_new(person)

    async def update(self, person: Person) -> None:
        self._unit_of_work.register_dirty(person)

    def _document_to_person(self, document: Mapping[str, Any]) -> Person:
        death_date_or_none = document["death_date"]
        if death_date_or_none:
            death_date = date.fromisoformat(death_date_or_none)
        else:
            death_date = None

        return Person(
            id=PersonId(UUID(document["id"])),
            first_name=document["first_name"],
            last_name=document["last_name"],
            sex=Sex(document["sex"]),
            birth_date=date.fromisoformat(document["birth_date"]),
            death_date=death_date,
        )
