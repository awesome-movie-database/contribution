# mypy: disable-error-code="arg-type"

import copy
from typing import Protocol, Sequence, Union

from motor.motor_asyncio import AsyncIOMotorClientSession

from contribution.domain import (
    Movie,
    User,
    Person,
    Role,
    Writer,
    CrewMember,
    Contribution,
    AddMovieContribution,
    EditMovieContribution,
    AddPersonContribution,
    EditPersonContribution,
    Achievement,
)
from .collection_committers import (
    CommitUserCollectionChanges,
    CommitMovieCollectionChanges,
    CommitPersonCollectionChanges,
    CommitRoleCollectionChanges,
    CommitWriterCollectionChanges,
    CommitCrewMemberCollectionChanges,
    CommitAddMovieContributionCollectionChanges,
    CommitEditMovieContributionCollectionChanges,
    CommitAddPersonContributionCollectionChanges,
    CommitEditPersonContributionCollectionChanges,
    CommitAchievementCollectionChanges,
)


type AnyModel = Union[
    Movie,
    User,
    Person,
    Role,
    Writer,
    CrewMember,
    Contribution,
    AddMovieContribution,
    EditMovieContribution,
    AddPersonContribution,
    EditPersonContribution,
    Achievement,
]


class CommitCollectionChanges[M: AnyModel](Protocol):
    async def __call__(
        self,
        *,
        new: Sequence[M],
        clean: Sequence[M],
        dirty: Sequence[M],
        deleted: Sequence[M],
    ) -> None:
        raise NotImplementedError


class MongoDBUnitOfWork:
    def __init__(
        self,
        commit_user_collection_changes: CommitUserCollectionChanges,
        commit_movie_collection_changes: CommitMovieCollectionChanges,
        commit_person_collection_changes: CommitPersonCollectionChanges,
        commit_role_collection_changes: CommitRoleCollectionChanges,
        commit_writer_collection_changes: CommitWriterCollectionChanges,
        commit_crew_member_collection_changes: (
            CommitCrewMemberCollectionChanges
        ),
        commit_add_movie_contribution_collection_changes: (
            CommitAddMovieContributionCollectionChanges
        ),
        commit_edit_movie_contribution_collection_changes: (
            CommitEditMovieContributionCollectionChanges
        ),
        commit_add_person_contribution_collection_changes: (
            CommitAddPersonContributionCollectionChanges
        ),
        commit_edit_person_contribution_collection_changes: (
            CommitEditPersonContributionCollectionChanges
        ),
        commit_achievement_collection_changes: (
            CommitAchievementCollectionChanges
        ),
        session: AsyncIOMotorClientSession,
    ):
        self._collection_changes_commiters: dict[
            type[AnyModel],
            CommitCollectionChanges,
        ] = {
            User: commit_user_collection_changes,
            Movie: commit_movie_collection_changes,
            Person: commit_person_collection_changes,
            Role: commit_role_collection_changes,
            Writer: commit_writer_collection_changes,
            CrewMember: commit_crew_member_collection_changes,
            AddMovieContribution: (
                commit_add_movie_contribution_collection_changes
            ),
            EditMovieContribution: (
                commit_edit_movie_contribution_collection_changes
            ),
            AddPersonContribution: (
                commit_add_person_contribution_collection_changes
            ),
            EditPersonContribution: (
                commit_edit_person_contribution_collection_changes
            ),
            Achievement: commit_achievement_collection_changes,
        }
        self._session = session

        self._new: dict[type[AnyModel], dict[int, AnyModel]] = {}
        self._clean: dict[type[AnyModel], dict[int, AnyModel]] = {}
        self._dirty: dict[type[AnyModel], dict[int, AnyModel]] = {}
        self._deleted: dict[type[AnyModel], dict[int, AnyModel]] = {}

    def register_new(self, model: AnyModel) -> None:
        model_id = id(model)

        new_models = self._new.get(type(model))
        if not new_models:
            self._new[type(model)] = {}

        self._new[type(model)][model_id] = model

    def register_clean(self, model: AnyModel) -> None:
        model_id = id(model)

        clean_models = self._clean.get(type(model))
        if not clean_models:
            self._clean[type(model)] = {}

        self._clean[type(model)][model_id] = copy.deepcopy(model)

    def register_dirty(self, model: AnyModel) -> None:
        model_id = id(model)

        new_models = self._new.get(type(model), {})
        if model_id in new_models:
            return

        dirty_models = self._dirty.get(type(model))
        if not dirty_models:
            self._dirty[type(model)] = {}

        self._dirty[type(model)][model_id] = model

    def register_deleted(self, model: AnyModel) -> None:
        model_id = id(model)

        new_models = self._new.get(type(model))
        if new_models and model_id in new_models:
            self._new[type(model)].pop(model_id)
            return

        dirty_models = self._dirty.get(type(model))
        clean_models = self._clean.get(type(model))

        if dirty_models:
            if not clean_models:
                message = f"No models of {type(model)} type registered"
                raise Exception(message)

            if model_id in dirty_models:
                self._dirty[type(model)].pop(model_id)
                self._clean[type(model)].pop(model_id)

        deleted_models = self._deleted.get(type(model))
        if not deleted_models:
            self._deleted[type(model)] = {}

        self._deleted[type(model)][model_id] = model

    async def commit(self) -> None:
        model_types = (
            User,
            Movie,
            Person,
            Role,
            Writer,
            CrewMember,
            AddMovieContribution,
            EditMovieContribution,
            AddPersonContribution,
            EditPersonContribution,
            Achievement,
        )
        for model_type in model_types:
            await self._collection_changes_commiters[model_type](
                new=self._new.get(model_type, {}).values(),
                clean=self._clean.get(model_type, {}).values(),
                dirty=self._dirty.get(model_type, {}).values(),
                deleted=self._deleted.get(model_type, {}).values(),
            )
        await self._session.commit_transaction()

    def __repr__(self) -> str:
        return (
            "UnitOfWork("
            f"new={self._new},"
            f"clean={self._clean},"
            f"dirty={self._dirty},"
            f"deleted={self._deleted})"
        )
