from typing import Any, Iterable, Optional
from uuid import UUID

from motor.motor_asyncio import AsyncIOMotorCollection

from contribution.domain import RoleId, MovieId, PersonId, Role
from contribution.infrastructure.database.identity_maps import (
    RoleMap,
)
from contribution.infrastructure.database.lock_factory import (
    MongoDBLockFactory,
)
from contribution.infrastructure.database.unit_of_work import (
    MongoDBUnitOfWork,
)


class RoleMapper:
    def __init__(
        self,
        role_map: RoleMap,
        collection: AsyncIOMotorCollection,
        lock_factory: MongoDBLockFactory,
        unit_of_work: MongoDBUnitOfWork,
    ):
        self._role_map = role_map
        self._collection = collection
        self._lock_factory = lock_factory
        self._unit_of_work = unit_of_work

    async def by_id(self, id: RoleId) -> Optional[Role]:
        role_from_map = self._role_map.by_id(id)
        if role_from_map:
            return role_from_map

        document_or_none = await self._collection.find_one(
            {"id": id.hex},
        )
        if document_or_none:
            role = self._document_to_role(document_or_none)
            self._role_map.save(role)
            self._unit_of_work.register_clean(role)
            return role

        return None

    async def list_by_ids(
        self,
        ids: Iterable[RoleId],
    ) -> list[Role]:
        roles_from_map = []
        for id in ids:
            role_from_map = self._role_map.by_id(id)
            if not role_from_map:
                break
            roles_from_map.append(role_from_map)
        else:
            return roles_from_map

        documents = await self._collection.find(
            {"id": {"$in": [id.hex for id in ids]}},
        ).to_list()

        roles = []
        for document in documents:
            role = self._document_to_role(document)
            self._role_map.save(role)
            self._unit_of_work.register_clean(role)
            roles.append(role)

        return roles

    async def save_many(self, roles: Iterable[Role]) -> None:
        for role in roles:
            self._role_map.save(role)
            self._unit_of_work.register_new(role)

    async def update(self, role: Role) -> None:
        self._unit_of_work.register_dirty(role)

    async def delete_many(self, roles: Iterable[Role]) -> None:
        for role in roles:
            self._unit_of_work.register_deleted(role)

    def _document_to_role(self, document: dict[str, Any]) -> Role:
        return Role(
            id=RoleId(UUID(document["id"])),
            movie_id=MovieId(UUID(document["movie_id"])),
            person_id=PersonId(UUID(document["person_id"])),
            character=document["character"],
            importance=document["importance"],
            is_spoiler=document["is_spoiler"],
        )
