from typing import Any, Sequence, Optional

from pymongo import InsertOne, UpdateOne, DeleteOne
from pymongo.errors import OperationFailure
from motor.motor_asyncio import AsyncIOMotorClientSession

from contribution.domain import User
from contribution.application import (
    UserIdIsAlreadyTakenError,
    UserNameIsAlreadyTakenError,
    UserEmailIsAlreadyTakenError,
)
from contribution.infrastructure.database.collections import (
    UserCollection,
)


class CommitUserCollectionChanges:
    def __init__(
        self,
        collection: UserCollection,
        session: AsyncIOMotorClientSession,
    ):
        self._collection = collection
        self._session = session

    async def __call__(
        self,
        *,
        new: Sequence[User],
        clean: Sequence[User],
        dirty: Sequence[User],
        deleted: Sequence[User],
    ) -> None:
        inserts = [InsertOne(self._user_to_document(user)) for user in new]
        updates = [
            UpdateOne(
                {"id": clean_user.id},
                self._pipeline_to_update_user(clean_user, dirty_user),
            )
            for clean_user, dirty_user in zip(clean, dirty)
        ]
        deletes = [DeleteOne({"id": user.id}) for user in deleted]

        changes: list[InsertOne, UpdateOne, DeleteOne] = [
            *inserts,
            *updates,
            *deletes,
        ]
        if changes:
            try:
                await self._collection.bulk_write(
                    requests=changes,
                    session=self._session,
                )
            except OperationFailure as e:
                await self._on_operation_failure_error(e)

    def _user_to_document(self, user: User) -> dict[str, Any]:
        document = {
            "id": user.id.hex,
            "name": user.name,
            "email": user.email,
            "telegram": user.telegram,
            "is_active": user.is_active,
            "rating": user.rating,
            "accepted_contributions_count": (
                user.accepted_contributions_count
            ),
            "rejected_contributions_count": (
                user.rejected_contributions_count
            ),
        }
        return document

    def _pipeline_to_update_user(
        self,
        clean: User,
        dirty: User,
    ) -> dict[str, Any]:
        pipeline = {"$set": {}}

        if clean.name != dirty.name:
            pipeline["$set"]["name"] = dirty.name
        if clean.email != dirty.email:
            pipeline["$set"]["email"] = dirty.email
        if clean.telegram != dirty.telegram:
            pipeline["$set"]["telegram"] = dirty.telegram
        if clean.is_active != dirty.is_active:
            pipeline["$set"]["is_active"] = dirty.is_active
        if clean.rating != dirty.rating:
            pipeline["$set"]["rating"] = dirty.rating
        if (
            clean.accepted_contributions_count
            != dirty.accepted_contributions_count
        ):
            pipeline["$set"][
                "accepted_contributions_count"
            ] = dirty.accepted_contributions_count
        if (
            clean.rejected_contributions_count
            != dirty.rejected_contributions_count
        ):
            pipeline["$set"][
                "rejected_contributions_count"
            ] = dirty.rejected_contributions_count

        return pipeline

    async def _on_operation_failure_error(
        self,
        error: OperationFailure,
    ) -> None:
        await self._session.abort_transaction()

        if not error.details:
            raise error

        write_errors: Optional[list[dict[str, Any]]] = error.details.get(
            "writeErrors",
        )
        if not write_errors:
            raise error

        first_write_error: dict[str, Any] = write_errors[0]
        first_write_error_code = first_write_error.get("code")
        if not first_write_error_code:
            message = (
                "First write error of write errors "
                "in OperationFailure details has no code"
            )
            raise ValueError(message)

        is_duplicate_error = first_write_error_code == 11000
        if not is_duplicate_error:
            raise error

        caused_error_key_value: Optional[
            dict[str, Any]
        ] = first_write_error.get("keyValue")
        if not caused_error_key_value:
            message = (
                "First write error of write errors "
                "in OperationFailure details has no 'KeyValue' field"
            )
            raise ValueError(message)

        caused_error_key = list(caused_error_key_value.keys())[0]
        if caused_error_key == "id":
            raise UserIdIsAlreadyTakenError()
        elif caused_error_key == "name":
            raise UserNameIsAlreadyTakenError()
        elif caused_error_key == "email":
            raise UserEmailIsAlreadyTakenError()

        message = (
            f"DuplicateError was caused by unexpected key: {caused_error_key}"
        )
        raise ValueError(message)
