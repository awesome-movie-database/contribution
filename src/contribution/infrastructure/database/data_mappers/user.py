from typing import Any, Mapping, Optional
from uuid import UUID

from contribution.domain import UserId, User
from contribution.infrastructure.database.collections import (
    UserCollection,
)
from contribution.infrastructure.database.identity_maps import (
    UserMap,
)
from contribution.infrastructure.database.lock_factory import (
    MongoDBLockFactory,
)
from contribution.infrastructure.database.unit_of_work import (
    MongoDBUnitOfWork,
)


class UserMapper:
    def __init__(
        self,
        user_map: UserMap,
        collection: UserCollection,
        lock_factory: MongoDBLockFactory,
        unit_of_work: MongoDBUnitOfWork,
    ):
        self._user_map = user_map
        self._collection = collection
        self._lock_factory = lock_factory
        self._unit_of_work = unit_of_work

    async def by_id(self, id: UserId) -> Optional[User]:
        user_from_map = self._user_map.by_id(id)
        if user_from_map:
            return user_from_map

        document = await self._collection.find_one(
            {"id": id.hex},
        )
        if document:
            user = self._document_to_user(document)
            self._user_map.save(user)
            self._unit_of_work.register_clean(user)
            return user

        return None

    async def by_name(self, name: str) -> Optional[User]:
        user_from_map = self._user_map.by_name(name)
        if user_from_map:
            return user_from_map

        document = await self._collection.find_one({"name": name})
        if document:
            user = self._document_to_user(document)
            self._user_map.save(user)
            self._unit_of_work.register_clean(user)
            return user

        return None

    async def by_email(self, email: str) -> Optional[User]:
        user_from_map = self._user_map.by_email(email)
        if user_from_map:
            return user_from_map

        document = await self._collection.find_one({"email": email})
        if document:
            user = self._document_to_user(document)
            self._user_map.save(user)
            self._unit_of_work.register_clean(user)
            return user

        return None

    async def by_telegram(self, telegram: str) -> Optional[User]:
        user_from_map = self._user_map.by_telegram(telegram)
        if user_from_map:
            return user_from_map

        document = await self._collection.find_one(
            {"telegram": telegram},
        )
        if document:
            user = self._document_to_user(document)
            self._user_map.save(user)
            self._unit_of_work.register_clean(user)
            return user

        return None

    async def acquire_by_id(self, id: UserId) -> Optional[User]:
        user_from_map = self._user_map.by_id(id)
        if user_from_map and self._user_map.is_acquired(user_from_map):
            return user_from_map

        document = await self._collection.find_one_and_update(
            {"id": id.hex},
            {"$set": {"lock": self._lock_factory()}},
        )
        if document:
            user = self._document_to_user(document)
            self._user_map.save_acquired(user)
            self._unit_of_work.register_clean(user)
            return user

        return None

    async def save(self, user: User) -> None:
        self._user_map.save(user)
        self._unit_of_work.register_new(user)

    async def update(self, user: User) -> None:
        self._unit_of_work.register_dirty(user)

    def _document_to_user(self, document: Mapping[str, Any]) -> User:
        return User(
            id=UserId(UUID(document["id"])),
            name=document["name"],
            email=document["email"],
            telegram=document["telegram"],
            is_active=document["is_active"],
            rating=document["rating"],
            accepted_contributions_count=document[
                "accepted_contributions_count"
            ],
            rejected_contributions_count=document[
                "rejected_contributions_count"
            ],
        )
