# mypy: disable-error-code="assignment"

from typing import Any, Iterable, Sequence

from pymongo import InsertOne, UpdateOne, DeleteOne
from motor.motor_asyncio import AsyncIOMotorClientSession

from contribution.domain import (
    ContributionRole,
    ContributionWriter,
    ContributionCrewMember,
    AddMovieContribution,
)
from contribution.infrastructure.database.collections import (
    AddMovieContributionCollection,
)


class CommitAddMovieContributionCollectionChanges:
    def __init__(
        self,
        collection: AddMovieContributionCollection,
        session: AsyncIOMotorClientSession,
    ):
        self._collection = collection
        self._session = session

    async def __call__(
        self,
        *,
        new: Sequence[AddMovieContribution],
        clean: Sequence[AddMovieContribution],
        dirty: Sequence[AddMovieContribution],
        deleted: Sequence[AddMovieContribution],
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
        await self._collection.bulk_write(
            requests=changes,
            session=self._session,
        )

    def _contribution_to_document(
        self,
        contribution: AddMovieContribution,
    ) -> dict[str, Any]:
        document = {
            "id": contribution.id.hex,
            "status": contribution.status,
            "author_id": contribution.author_id.hex,
            "eng_title": contribution.eng_title,
            "original_title": contribution.original_title,
            "release_date": contribution.release_date.isoformat(),
            "countries": list(contribution.countries),
            "genres": list(contribution.genres),
            "mpaa": contribution.mpaa,
            "duration": contribution.duration,
            "photos": list(contribution.photos),
        }

        if contribution.status_updated_at:
            document[
                "status_updated_at"
            ] = contribution.status_updated_at.isoformat()
        else:
            document["status_updated_at"] = None
        if contribution.budget:
            document["budget"] = {
                "amount": contribution.budget.amount,
                "currency": contribution.budget.currency,
            }
        else:
            document["budget"] = None
        if contribution.revenue:
            document["revenue"] = {
                "amount": contribution.revenue.amount,
                "currency": contribution.revenue.currency,
            }
        else:
            document["revenue"] = None

        document["roles"] = self._contribution_roles_to_dict_list(
            contribution_roles=contribution.roles,
        )
        document["writers"] = self._contribution_writers_to_dict_list(
            contribution_writers=contribution.writers,
        )
        document["crew"] = self._contribution_crew_to_dict_list(
            contribution_crew=contribution.crew,
        )

        return document

    def _pipeline_to_update_contribution(
        self,
        clean: AddMovieContribution,
        dirty: AddMovieContribution,
    ) -> dict[str, Any]:
        pipeline = {"$set": {}}

        if clean.status != dirty.status:
            pipeline["$set"]["status"] = dirty.status
        if clean.status_updated_at != dirty.status_updated_at:
            if dirty.status_updated_at:
                pipeline["$set"][
                    "status_updated_at"
                ] = dirty.status_updated_at.isoformat()
            else:
                pipeline["$set"]["status_updated_at"] = None
        if clean.eng_title != dirty.eng_title:
            pipeline["$set"]["eng_title"] = dirty.eng_title
        if clean.original_title != dirty.original_title:
            pipeline["$set"]["original_title"] = dirty.original_title
        if clean.release_date != dirty.release_date:
            pipeline["$set"]["release_date"] = dirty.release_date.isoformat()
        if clean.countries != dirty.countries:
            pipeline["$set"]["countries"] = list(dirty.countries)
        if clean.genres != dirty.genres:
            pipeline["$set"]["genres"] = list(dirty.genres)
        if clean.mpaa != dirty.mpaa:
            pipeline["$set"]["mpaa"] = dirty.mpaa
        if clean.duration != dirty.duration:
            pipeline["$set"]["duration"] = dirty.duration
        if clean.budget != dirty.budget:
            if dirty.budget:
                pipeline["$set"]["budget"] = {
                    "amount": str(dirty.budget.amount),
                    "currency": dirty.budget.currency,
                }
            else:
                pipeline["$set"]["budget"] = None
        if clean.revenue != dirty.revenue:
            if dirty.revenue:
                pipeline["$set"]["revenue"] = {
                    "amount": str(dirty.revenue.amount),
                    "currency": dirty.revenue.currency,
                }
            else:
                pipeline["$set"]["revenue"] = None
        if clean.roles != dirty.roles:
            pipeline["$set"]["roles"] = self._contribution_roles_to_dict_list(
                contribution_roles=dirty.roles,
            )
        if clean.writers != dirty.writers:
            pipeline["$set"][
                "writers"
            ] = self._contribution_writers_to_dict_list(
                contribution_writers=dirty.writers,
            )
        if clean.crew != dirty.crew:
            pipeline["$set"]["crew"] = self._contribution_crew_to_dict_list(
                contribution_crew=dirty.crew,
            )

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
                "writing": contribution_writer.writing,
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
                "membership": contribution_crew_member.membership,
            }
            contribution_crew_as_dict_list.append(
                contribution_crew_member_as_dict,
            )
        return contribution_crew_as_dict_list
