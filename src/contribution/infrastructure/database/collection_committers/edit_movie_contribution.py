# mypy: disable-error-code="assignment"

from typing import Any, Iterable, Sequence

from pymongo import InsertOne, UpdateOne, DeleteOne
from motor.motor_asyncio import AsyncIOMotorClientSession

from contribution.domain import (
    ContributionRole,
    ContributionWriter,
    ContributionCrewMember,
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
        contribution: EditMovieContribution,
    ) -> dict[str, Any]:
        document = {
            "id": contribution.id.hex,
            "status": contribution.status,
            "author_id": contribution.author_id.hex,
            "movie_id": contribution.movie_id.hex,
            "add_photos": list(contribution.add_photos),
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

        document["add_roles"] = self._contribution_roles_to_dict_list(
            contribution_roles=contribution.add_roles,
        )
        document["remove_roles"] = [
            role_id.hex for role_id in contribution.remove_roles
        ]
        document["add_writers"] = self._contribution_writers_to_dict_list(
            contribution_writers=contribution.add_writers,
        )
        document["remove_writers"] = [
            writer_id.hex for writer_id in contribution.remove_writers
        ]
        document["add_crew"] = self._contribution_crew_to_dict_list(
            contribution_crew=contribution.add_crew,
        )
        document["remove_crew"] = [
            crew_member_id.hex for crew_member_id in contribution.remove_crew
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
        if clean.add_roles != dirty.add_roles:
            pipeline["$set"][
                "add_roles"
            ] = self._contribution_roles_to_dict_list(
                contribution_roles=dirty.add_roles,
            )
        if clean.remove_roles != dirty.remove_roles:
            pipeline["$set"]["remove_roles"] = [
                role_id.hex for role_id in dirty.remove_roles
            ]
        if clean.add_writers != dirty.add_writers:
            pipeline["$set"][
                "add_writers"
            ] = self._contribution_writers_to_dict_list(
                contribution_writers=dirty.add_writers,
            )
        if clean.remove_writers != dirty.remove_writers:
            pipeline["$set"]["remove_writers"] = [
                writer_id.hex for writer_id in dirty.remove_writers
            ]
        if clean.add_crew != dirty.add_crew:
            pipeline["$set"][
                "add_crew"
            ] = self._contribution_crew_to_dict_list(
                contribution_crew=dirty.add_crew,
            )
        if clean.remove_crew != dirty.remove_crew:
            pipeline["$set"]["remove_crew"] = [
                writer_id.hex for writer_id in dirty.remove_writers
            ]
        if clean.add_photos != dirty.add_photos:
            pipeline["$set"]["add_photos"] = list(dirty.add_photos)

        return pipeline

    def _contribution_roles_to_dict_list(
        self,
        contribution_roles: Iterable[ContributionRole],
    ) -> list[dict[str, Any]]:
        contribution_roles_as_dict_list = []
        for contribution_role in contribution_roles:
            contribution_role_as_dict = {
                "person_id": contribution_role.person_id.hex,
                "character": contribution_role.character,
                "importance": contribution_role.importance,
                "is_spoiler": contribution_role.is_spoiler,
            }
            contribution_roles_as_dict_list.append(
                contribution_role_as_dict,
            )
        return contribution_roles_as_dict_list

    def _contribution_writers_to_dict_list(
        self,
        contribution_writers: Iterable[ContributionWriter],
    ) -> list[dict[str, Any]]:
        contribution_writers_as_dict_list = []
        for contribution_writer in contribution_writers:
            contribution_writer_as_dict = {
                "person_id": contribution_writer.person_id.hex,
                "writing": contribution_writer.writing.value,
            }
            contribution_writers_as_dict_list.append(
                contribution_writer_as_dict,
            )
        return contribution_writers_as_dict_list

    def _contribution_crew_to_dict_list(
        self,
        contribution_crew: Iterable[ContributionCrewMember],
    ) -> list[dict[str, Any]]:
        contribution_crew_as_dict_list = []
        for contribution_crew_member in contribution_crew:
            contribution_crew_member_as_dict = {
                "person_id": contribution_crew_member.person_id.hex,
                "membership": contribution_crew_member.membership.value,
            }
            contribution_crew_as_dict_list.append(
                contribution_crew_member_as_dict,
            )
        return contribution_crew_as_dict_list
