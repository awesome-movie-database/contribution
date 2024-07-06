from typing import Any, Iterable, Mapping, Optional
from uuid import UUID

from motor.motor_asyncio import AsyncIOMotorClientSession

from contribution.domain import RoleId, MovieId, PersonId, Role
from contribution.infrastructure.database.collections import (
    RoleCollection,
)
from contribution.infrastructure.database.identity_maps import (
    RoleMap,
)
from contribution.infrastructure.database.unit_of_work import (
    MongoDBUnitOfWork,
)


class RoleMapper:
    def __init__(
        self,
        role_map: RoleMap,
        role_collection: RoleCollection,
        unit_of_work: MongoDBUnitOfWork,
        session: AsyncIOMotorClientSession,
    ):
        self._role_map = role_map
        self._role_collection = role_collection
        self._unit_of_work = unit_of_work
        self._session = session

    async def by_id(self, id: RoleId) -> Optional[Role]:
        role_from_map = self._role_map.by_id(id)
        if role_from_map:
            return role_from_map

        document = await self._role_collection.find_one(
            {"id": id.hex},
            session=self._session,
        )
        if document:
            role = self._document_to_role(document)
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

        documents = await self._role_collection.find(
            {"id": {"$in": [id.hex for id in ids]}},
            session=self._session,
        ).to_list(None)

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

    def _document_to_role(self, document: Mapping[str, Any]) -> Role:
        return Role(
            id=RoleId(UUID(document["id"])),
            movie_id=MovieId(UUID(document["movie_id"])),
            person_id=PersonId(UUID(document["person_id"])),
            character=document["character"],
            importance=document["importance"],
            is_spoiler=document["is_spoiler"],
        )
