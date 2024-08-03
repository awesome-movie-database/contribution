# mypy: disable-error-code="assignment"

from typing import Any, Iterable, Sequence

from pymongo import InsertOne, UpdateOne, DeleteOne
from motor.motor_asyncio import AsyncIOMotorClientSession

from contribution.domain import (
    MovieRole,
    MovieWriter,
    MovieCrewMember,
    EditMovieContribution,
)
from contribution.infrastructure.database.collections import (
    EditMovieContributionCollection,
)


class CommitEditMovieContributionCollectionChanges:
    def __init__(
        self,
        collection: EditMovieContributionCollection,
        session: AsyncIOMotorClientSession,
    ):
        self._collection = collection
        self._session = session

    async def __call__(
        self,
        *,
        new: Sequence[EditMovieContribution],
        clean: Sequence[EditMovieContribution],
        dirty: Sequence[EditMovieContribution],
        deleted: Sequence[EditMovieContribution],
    ) -> None:
        inserts = [
            InsertOne(self._contribution_to_document(contribution))
            for contribution in new
        ]
        updates = [
            UpdateOne(
                {"id": clean_contribution.id.hex},
                self._pipeline_to_update_contribution(
                    clean_contribution,
                    dirty_contribution,
                ),
            )
            for clean_contribution, dirty_contribution in zip(clean, dirty)
        ]
        deletes = [
            DeleteOne({"id": contribution.id.hex}) for contribution in deleted
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
        contribution: EditMovieContribution,
    ) -> dict[str, Any]:
        document = {
            "id": contribution.id.hex,
            "status": contribution.status,
            "author_id": contribution.author_id.hex,
            "movie_id": contribution.movie_id.hex,
            "photos_to_add": list(contribution.photos_to_add),
        }

        if contribution.status_updated_at:
            document[
                "status_updated_at"
            ] = contribution.status_updated_at.isoformat()
        else:
            document["status_updated_at"] = None
        if contribution.eng_title.is_set:
            document["eng_title"] = contribution.eng_title.value
        if contribution.original_title.is_set:
            document["original_title"] = contribution.original_title.value
        if contribution.release_date.is_set:
            document[
                "release_date"
            ] = contribution.release_date.value.isoformat()
        if contribution.countries.is_set:
            document["countries"] = list(contribution.countries.value)
        if contribution.genres.is_set:
            document["genres"] = list(contribution.genres.value)
        if contribution.mpaa.is_set:
            document["mpaa"] = contribution.mpaa.value
        if contribution.duration.is_set:
            document["duration"] = contribution.duration.value
        if contribution.budget.is_set:
            budget = contribution.budget.value
            if budget:
                document["budget"] = {
                    "amount": str(budget.amount),
                    "currency": budget.currency,
                }
            else:
                document["budget"] = None
        if contribution.revenue.is_set:
            revenue = contribution.revenue.value
            if revenue:
                document["revenue"] = {
                    "amount": str(revenue.amount),
                    "currency": revenue.currency,
                }
            else:
                document["revenue"] = None

        document["roles_to_add"] = self._movie_roles_to_dicts(
            movie_roles=contribution.roles_to_add,
        )
        document["roles_to_more"] = [
            role_id.hex for role_id in contribution.roles_to_remove
        ]
        document["writers_to_add"] = self._movie_writers_to_dicts(
            movie_writers=contribution.writers_to_add,
        )
        document["writers_to_remove"] = [
            writer_id.hex for writer_id in contribution.writers_to_remove
        ]
        document["crew_to_add"] = self._movie_crew_to_dicts(
            movie_crew=contribution.crew_to_add,
        )
        document["crew_to_remove"] = [
            crew_member_id.hex
            for crew_member_id in contribution.crew_to_remove
        ]

        return document

    def _pipeline_to_update_contribution(
        self,
        clean: EditMovieContribution,
        dirty: EditMovieContribution,
    ) -> dict[str, Any]:
        pipeline = {"$set": {}, "$unset": {}}

        if clean.status != dirty.status:
            pipeline["$set"]["status"] = dirty.status.value
        if clean.status_updated_at != dirty.status_updated_at:
            if dirty.status_updated_at:
                pipeline["$set"][
                    "status_updated_at"
                ] = dirty.status_updated_at.isoformat()
            else:
                pipeline["$set"]["status_updated_at"] = None
        if clean.eng_title != dirty.eng_title:
            if dirty.eng_title.is_set:
                pipeline["$set"]["eng_title"] = dirty.eng_title.value
            else:
                pipeline["$unset"]["eng_title"] = ""
        if clean.original_title != dirty.original_title:
            if dirty.original_title.is_set:
                pipeline["$set"]["original_title"] = dirty.original_title.value
            else:
                pipeline["$unset"]["original_title"] = ""
        if clean.release_date != dirty.release_date:
            if dirty.release_date.is_set:
                pipeline["$set"][
                    "release_date"
                ] = dirty.release_date.value.isoformat()
            else:
                pipeline["$unset"]["release_date"] = ""
        if clean.countries != dirty.countries:
            if dirty.countries.is_set:
                pipeline["$set"]["countries"] = list(dirty.countries.value)
            else:
                pipeline["$unset"]["countries"] = ""
        if clean.genres != dirty.genres:
            if dirty.genres.is_set:
                pipeline["$set"]["genres"] = [
                    genre.value for genre in dirty.genres.value
                ]
            else:
                pipeline["$unset"]["genres"] = ""
        if clean.mpaa != dirty.mpaa:
            if dirty.mpaa.is_set:
                pipeline["$set"]["mpaa"] = dirty.mpaa.value.value
            else:
                pipeline["$unset"]["mpaa"] = ""
        if clean.duration != dirty.duration:
            if dirty.duration.is_set:
                pipeline["$set"]["duration"] = dirty.duration.value
            else:
                pipeline["$unset"]["duration"] = ""
        if clean.budget != dirty.budget:
            if dirty.budget.is_set:
                budget = dirty.budget.value
                if budget:
                    pipeline["$set"]["budget"] = {
                        "amount": str(budget.amount),
                        "currency": budget.currency,
                    }
                else:
                    pipeline["$set"]["budget"] = None
            else:
                pipeline["$unset"]["budget"] = ""
        if clean.revenue != dirty.revenue:
            if dirty.revenue.is_set:
                revenue = dirty.revenue.value
                if revenue:
                    pipeline["$set"]["revenue"] = {
                        "amount": str(revenue.amount),
                        "currency": revenue.currency,
                    }
                else:
                    pipeline["$set"]["revenue"] = None
            else:
                pipeline["$unset"]["revenue"] = ""
        if clean.roles_to_add != dirty.roles_to_add:
            pipeline["$set"]["roles_to_add"] = self._movie_roles_to_dicts(
                dirty.roles_to_add,
            )
        if clean.roles_to_remove != dirty.roles_to_remove:
            pipeline["$set"]["roles_to_remove"] = [
                role_id.hex for role_id in dirty.roles_to_remove
            ]
        if clean.writers_to_add != dirty.writers_to_add:
            pipeline["$set"]["writers_to_add"] = self._movie_writers_to_dicts(
                dirty.writers_to_add,
            )
        if clean.writers_to_remove != dirty.writers_to_remove:
            pipeline["$set"]["writers_to_remove"] = [
                writer_id.hex for writer_id in dirty.writers_to_remove
            ]
        if clean.crew_to_add != dirty.crew_to_add:
            pipeline["$set"]["crew_to_add"] = self._movie_crew_to_dicts(
                dirty.crew_to_add,
            )
        if clean.crew_to_remove != dirty.crew_to_remove:
            pipeline["$set"]["crew_to_remove"] = [
                writer_id.hex for writer_id in dirty.writers_to_remove
            ]
        if clean.photos_to_add != dirty.photos_to_add:
            pipeline["$set"]["photos_to_add"] = list(dirty.photos_to_add)

        return pipeline

    def _movie_roles_to_dicts(
        self,
        movie_roles: Iterable[MovieRole],
    ) -> list[dict[str, Any]]:
        movie_roles_as_dicts = []
        for movie_role in movie_roles:
            movie_role_as_dict = {
                "id": movie_role.id.hex,
                "person_id": movie_role.person_id.hex,
                "character": movie_role.character,
                "importance": movie_role.importance,
                "is_spoiler": movie_role.is_spoiler,
            }
            movie_roles_as_dicts.append(movie_role_as_dict)

        return movie_roles_as_dicts

    def _movie_writers_to_dicts(
        self,
        movie_writers: Iterable[MovieWriter],
    ) -> list[dict[str, Any]]:
        movie_writers_as_dicts = []
        for movie_writer in movie_writers:
            movie_writer_as_dict = {
                "id": movie_writer.id.hex,
                "person_id": movie_writer.person_id.hex,
                "writing": movie_writer.writing,
            }
            movie_writers_as_dicts.append(movie_writer_as_dict)

        return movie_writers_as_dicts

    def _movie_crew_to_dicts(
        self,
        movie_crew: Iterable[MovieCrewMember],
    ) -> list[dict[str, Any]]:
        movie_crew_as_dicts = []
        for movie_crew_member in movie_crew:
            movie_crew_member_as_dict = {
                "id": movie_crew_member.id.hex,
                "person_id": movie_crew_member.person_id.hex,
                "membership": movie_crew_member.membership,
            }
            movie_crew_as_dicts.append(movie_crew_member_as_dict)

        return movie_crew_as_dicts
