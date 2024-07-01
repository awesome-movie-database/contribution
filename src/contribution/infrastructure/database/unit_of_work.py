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


type AnyEntity = Union[
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


class CommitCollectionChanges[E: AnyEntity](Protocol):
    async def __call__(
        self,
        *,
        new: Sequence[E],
        clean: Sequence[E],
        dirty: Sequence[E],
        deleted: Sequence[E],
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
            type[AnyEntity],
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

        self._new: dict[type[AnyEntity], dict[int, AnyEntity]] = {}
        self._clean: dict[type[AnyEntity], dict[int, AnyEntity]] = {}
        self._dirty: dict[type[AnyEntity], dict[int, AnyEntity]] = {}
        self._deleted: dict[type[AnyEntity], dict[int, AnyEntity]] = {}

    def register_new(self, entity: AnyEntity) -> None:
        entity_id = id(entity)
        self._new[type(entity)][entity_id] = entity

    def register_clean(self, entity: AnyEntity) -> None:
        entity_id = id(entity)
        self._clean[type(entity)][entity_id] = copy.deepcopy(entity)

    def register_dirty(self, entity: AnyEntity) -> None:
        entity_id = id(entity)
        if entity_id not in self._new[type(entity)]:
            self._dirty[type(entity)][entity_id] = entity

    def register_deleted(self, entity: AnyEntity) -> None:
        entity_id = id(entity)

        if entity_id in self._new[type(entity)]:
            self._new[type(entity)].pop(entity_id)
            return
        if entity_id in self._dirty[type(entity)]:
            self._clean[type(entity)].pop(entity_id)
            self._dirty[type(entity)].pop(entity_id)

        self._deleted[type(entity)][entity_id] = entity

    async def commit(self) -> None:
        entity_types = (
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
        for entity_type in entity_types:
            await self._collection_changes_commiters[entity_type](
                new=self._new[entity_type].values(),
                clean=self._clean[entity_type].values(),
                dirty=self._dirty[entity_type].values(),
                deleted=self._deleted[entity_type].values(),
            )
        await self._session.commit_transaction()
