import asyncio

import pytest
from uuid_extensions import uuid7
from motor.motor_asyncio import (
    AsyncIOMotorClient,
    AsyncIOMotorClientSession,
    AsyncIOMotorDatabase,
)

from contribution.domain import UserId, User
from contribution.application import UserIdIsAlreadyTakenError
from contribution.infrastructure import (
    user_collection_factory,
    movie_collection_factory,
    person_collection_factory,
    role_collection_factory,
    writer_collection_factory,
    crew_member_collection_factory,
    add_movie_contribution_collection_factory,
    edit_movie_contribution_collection_factory,
    add_person_contribution_collection_factory,
    edit_person_contribution_collection_factory,
    achievement_collection_factory,
    UserMap,
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
    UserMapper,
    MongoDBLockFactory,
    MongoDBUnitOfWork,
    motor_database_factory,
)


async def unit_of_work_factory(
    motor_database: AsyncIOMotorDatabase,
    motor_session: AsyncIOMotorClientSession,
) -> MongoDBUnitOfWork:
    user_collection = await user_collection_factory(motor_database)
    movie_collection = await movie_collection_factory(motor_database)
    person_collection = await person_collection_factory(motor_database)
    role_collection = await role_collection_factory(motor_database)
    writer_collection = await writer_collection_factory(motor_database)
    crew_member_collection = await crew_member_collection_factory(
        motor_database,
    )
    add_movie_contribution_collection = (
        await add_movie_contribution_collection_factory(motor_database)
    )
    edit_movie_contribution_collection = (
        await edit_movie_contribution_collection_factory(motor_database)
    )
    add_person_contribution_collection = (
        await add_person_contribution_collection_factory(motor_database)
    )
    edit_person_contribution_collection = (
        await edit_person_contribution_collection_factory(motor_database)
    )
    achievement_collection = await achievement_collection_factory(
        motor_database,
    )

    return MongoDBUnitOfWork(
        commit_user_collection_changes=(
            CommitUserCollectionChanges(
                collection=user_collection,
                session=motor_session,
            )
        ),
        commit_movie_collection_changes=(
            CommitMovieCollectionChanges(
                collection=movie_collection,
                session=motor_session,
            )
        ),
        commit_person_collection_changes=(
            CommitPersonCollectionChanges(
                collection=person_collection,
                session=motor_session,
            )
        ),
        commit_role_collection_changes=(
            CommitRoleCollectionChanges(
                collection=role_collection,
                session=motor_session,
            )
        ),
        commit_writer_collection_changes=(
            CommitWriterCollectionChanges(
                collection=writer_collection,
                session=motor_session,
            )
        ),
        commit_crew_member_collection_changes=(
            CommitCrewMemberCollectionChanges(
                collection=crew_member_collection,
                session=motor_session,
            )
        ),
        commit_add_movie_contribution_collection_changes=(
            CommitAddMovieContributionCollectionChanges(
                collection=add_movie_contribution_collection,
                session=motor_session,
            )
        ),
        commit_edit_movie_contribution_collection_changes=(
            CommitEditMovieContributionCollectionChanges(
                collection=edit_movie_contribution_collection,
                session=motor_session,
            )
        ),
        commit_add_person_contribution_collection_changes=(
            CommitAddPersonContributionCollectionChanges(
                collection=add_person_contribution_collection,
                session=motor_session,
            )
        ),
        commit_edit_person_contribution_collection_changes=(
            CommitEditPersonContributionCollectionChanges(
                collection=edit_person_contribution_collection,
                session=motor_session,
            )
        ),
        commit_achievement_collection_changes=(
            CommitAchievementCollectionChanges(
                collection=achievement_collection,
                session=motor_session,
            )
        ),
        session=motor_session,
    )


async def save_user_to_database(
    *,
    user: User,
    user_mapper: UserMapper,
    unit_of_work: MongoDBUnitOfWork,
) -> None:
    await user_mapper.save(user)
    await unit_of_work.commit()


async def save_users_to_database_at_same_time(
    *users: User,
    motor_client: AsyncIOMotorClient,
) -> None:
    motor_sessions = []
    motor_databases = []
    opened_transactions = []
    unit_of_works = []
    user_mappers = []

    for _ in users:
        motor_session = await motor_client.start_session()
        opened_transaction = (
            await motor_session.start_transaction().__aenter__()
        )
        motor_database = motor_database_factory(motor_session)

        unit_of_work = await unit_of_work_factory(
            motor_database=motor_database,
            motor_session=motor_session,
        )
        user_mapper = UserMapper(
            user_map=UserMap(),
            user_collection=await user_collection_factory(motor_database),
            lock_factory=MongoDBLockFactory(),
            unit_of_work=unit_of_work,
            session=motor_session,
        )

        motor_sessions.append(motor_session)
        motor_databases.append(motor_database)
        opened_transactions.append(opened_transaction)
        unit_of_works.append(unit_of_work)
        user_mappers.append(user_mapper)

    coros = []
    for user, user_mapper, unit_of_work in zip(
        users,
        user_mappers,
        unit_of_works,
    ):
        coro = save_user_to_database(
            user=user,
            user_mapper=user_mapper,
            unit_of_work=unit_of_work,
        )
        coros.append(coro)

    try:
        await asyncio.gather(*coros)
    finally:
        for opened_transaction in opened_transactions:
            await opened_transaction.__aexit__(None, None, None)


@pytest.mark.skip("This test is an artifact created during development")
@pytest.mark.usefixtures("clear_database")
async def test_saving_two_users_with_same_id_to_database_at_same_time_should_raise_error(
    motor_client: AsyncIOMotorClient,
):
    common_user_id = UserId(uuid7())

    john_doe = User(
        id=common_user_id,
        name="JohnDoe",
        email=None,
        telegram=None,
        is_active=True,
        rating=0,
        accepted_contributions_count=0,
        rejected_contributions_count=0,
    )
    ivan_ivanov = User(
        id=common_user_id,
        name="IvanIvanov",
        email=None,
        telegram=None,
        is_active=True,
        rating=0,
        accepted_contributions_count=0,
        rejected_contributions_count=0,
    )

    with pytest.raises(UserIdIsAlreadyTakenError):
        await save_users_to_database_at_same_time(
            john_doe,
            ivan_ivanov,
            motor_client=motor_client,
        )
