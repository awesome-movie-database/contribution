from typing import Any, Iterable, Optional
from uuid import UUID

from motor.motor_asyncio import AsyncIOMotorCollection

from contribution.domain import (
    CrewMembership,
    CrewMemberId,
    MovieId,
    PersonId,
    CrewMember,
)
from contribution.infrastructure.database.identity_maps import (
    CrewMemberMap,
)
from contribution.infrastructure.database.lock_factory import (
    MongoDBLockFactory,
)
from contribution.infrastructure.database.unit_of_work import (
    MongoDBUnitOfWork,
)


class CrewMemberMapper:
    def __init__(
        self,
        crew_member_map: CrewMemberMap,
        collection: AsyncIOMotorCollection,
        lock_factory: MongoDBLockFactory,
        unit_of_work: MongoDBUnitOfWork,
    ):
        self._crew_member_map = crew_member_map
        self._collection = collection
        self._lock_factory = lock_factory
        self._unit_of_work = unit_of_work

    async def by_id(self, id: CrewMemberId) -> Optional[CrewMember]:
        crew_member_from_map = self._crew_member_map.by_id(id)
        if crew_member_from_map:
            return crew_member_from_map

        document_or_none = await self._collection.find_one(
            {"id": id.hex},
        )
        if document_or_none:
            role = self._document_to_crew_member(document_or_none)
            self._crew_member_map.save(role)
            self._unit_of_work.register_clean(role)
            return role

        return None

    async def list_by_ids(
        self,
        ids: Iterable[CrewMemberId],
    ) -> list[CrewMember]:
        crew_members_from_map = []
        for id in ids:
            crew_member_from_map = self._crew_member_map.by_id(id)
            if not crew_member_from_map:
                break
            crew_members_from_map.append(crew_member_from_map)
        else:
            return crew_members_from_map

        documents = await self._collection.find(
            {"id": {"$in": [id.hex for id in ids]}},
        ).to_list()

        crew_members = []
        for document in documents:
            role = self._document_to_crew_member(document)
            self._crew_member_map.save(role)
            self._unit_of_work.register_clean(role)
            crew_members.append(role)

        return crew_members

    async def save_many(self, crew_members: Iterable[CrewMember]) -> None:
        for crew_member in crew_members:
            self._crew_member_map.save(crew_member)
            self._unit_of_work.register_new(crew_member)

    async def update(self, crew_member: CrewMember) -> None:
        self._unit_of_work.register_dirty(crew_member)

    async def delete_many(self, crew_members: Iterable[CrewMember]) -> None:
        for crew_member in crew_members:
            self._unit_of_work.register_deleted(crew_member)

    def _document_to_crew_member(self, document: dict[str, Any]) -> CrewMember:
        return CrewMember(
            id=CrewMemberId(UUID(document["id"])),
            movie_id=MovieId(UUID(document["movie_id"])),
            person_id=PersonId(UUID(document["person_id"])),
            membership=CrewMembership(document["membership"]),
        )
