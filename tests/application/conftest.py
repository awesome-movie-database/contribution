from unittest.mock import AsyncMock
from typing import AsyncGenerator

import pytest
from motor.motor_asyncio import (
    AsyncIOMotorClient,
    AsyncIOMotorClientSession,
    AsyncIOMotorDatabase,
)
from redis.asyncio import Redis

from contribution.application import OnEventOccurred
from contribution.infrastructure import (
    UserCollection,
    MovieCollection,
    PersonCollection,
    RoleCollection,
    WriterCollection,
    CrewMemberCollection,
    AddMovieContributionCollection,
    EditMovieContributionCollection,
    AddPersonContributionCollection,
    EditPersonContributionCollection,
    AchievementCollection,
    PermissionsCollection,
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
    permissions_collection_factory,
    UserMap,
    MovieMap,
    PersonMap,
    RoleMap,
    WriterMap,
    CrewMemberMap,
    AddMovieContributionMap,
    EditMovieContributionMap,
    AddPersonContributionMap,
    EditPersonContributionMap,
    AchievementMap,
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
    MovieMapper,
    PersonMapper,
    RoleMapper,
    WriterMapper,
    CrewMemberMapper,
    AddMovieContributionMapper,
    EditMovieContributionMapper,
    AddPersonContributionMapper,
    EditPersonContributionMapper,
    AchievementMapper,
    PermissionsMapper,
    MongoDBLockFactory,
    MongoDBUnitOfWork,
    PermissionsCache,
    PermissionsStorage,
    PhotoStorage,
    MongoDBConfig,
    RedisConfig,
    motor_client_factory,
    motor_session_factory,
    motor_database_factory,
    redis_factory,
    env_var_by_key,
)


@pytest.fixture(scope="session")
def motor_client() -> AsyncIOMotorClient:
    mongodb_config = MongoDBConfig(
        username=env_var_by_key("TEST_MONGODB_USER"),
        password=env_var_by_key("TEST_MONGODB_PASSWORD"),
        host=env_var_by_key("TEST_MONGODB_HOST"),
        port=int(env_var_by_key("TEST_MONGODB_PORT")),
    )
    motor_client = motor_client_factory(mongodb_config)

    return motor_client


@pytest.fixture(scope="session")
def redis_client() -> Redis:
    redis_config = RedisConfig(
        url=env_var_by_key("TEST_REDIS_URL"),
    )
    redis_ = redis_factory(redis_config)

    return redis_


@pytest.fixture(scope="session")
def photo_gateway() -> PhotoStorage:
    return AsyncMock()


@pytest.fixture(scope="session")
def on_event_occurred() -> OnEventOccurred:
    return AsyncMock()


@pytest.fixture
async def motor_session(
    motor_client: AsyncIOMotorClient,
) -> AsyncGenerator[AsyncIOMotorClientSession, None]:
    return motor_session_factory(motor_client)


@pytest.fixture
def motor_database(
    motor_session: AsyncIOMotorClientSession,
) -> AsyncIOMotorDatabase:
    return motor_database_factory(motor_session)


@pytest.fixture
def user_collection(
    motor_database: AsyncIOMotorDatabase,
) -> UserCollection:
    return user_collection_factory(motor_database)


@pytest.fixture
def movie_collection(
    motor_database: AsyncIOMotorDatabase,
) -> MovieCollection:
    return movie_collection_factory(motor_database)


@pytest.fixture
def person_collection(
    motor_database: AsyncIOMotorDatabase,
) -> PersonCollection:
    return person_collection_factory(motor_database)


@pytest.fixture
def role_collection(
    motor_database: AsyncIOMotorDatabase,
) -> RoleCollection:
    return role_collection_factory(motor_database)


@pytest.fixture
def writer_collection(
    motor_database: AsyncIOMotorDatabase,
) -> WriterCollection:
    return writer_collection_factory(motor_database)


@pytest.fixture
def crew_member_collection(
    motor_database: AsyncIOMotorDatabase,
) -> CrewMemberCollection:
    return crew_member_collection_factory(motor_database)


@pytest.fixture
def add_movie_contribution_collection(
    motor_database: AsyncIOMotorDatabase,
) -> AddMovieContributionCollection:
    return add_movie_contribution_collection_factory(motor_database)


@pytest.fixture
def edit_movie_contribution_collection(
    motor_database: AsyncIOMotorDatabase,
) -> EditMovieContributionCollection:
    return edit_movie_contribution_collection_factory(motor_database)


@pytest.fixture
def add_person_contribution_collection(
    motor_database: AsyncIOMotorDatabase,
) -> AddPersonContributionCollection:
    return add_person_contribution_collection_factory(motor_database)


@pytest.fixture
def edit_person_contribution_collection(
    motor_database: AsyncIOMotorDatabase,
) -> EditPersonContributionCollection:
    return edit_person_contribution_collection_factory(motor_database)


@pytest.fixture
def achievement_collection(
    motor_database: AsyncIOMotorDatabase,
) -> AchievementCollection:
    return achievement_collection_factory(motor_database)


@pytest.fixture
def permissions_collection(
    motor_database: AsyncIOMotorDatabase,
) -> PermissionsCollection:
    return permissions_collection_factory(motor_database)


@pytest.fixture
def unit_of_work(
    user_collection: UserCollection,
    movie_collection: MovieCollection,
    person_collection: PersonCollection,
    role_collection: RoleCollection,
    writer_collection: WriterCollection,
    crew_member_collection: CrewMemberCollection,
    add_movie_contribution_collection: AddMovieContributionCollection,
    edit_movie_contribution_collection: EditMovieContributionCollection,
    add_person_contribution_collection: AddPersonContributionCollection,
    edit_person_contribution_collection: EditPersonContributionCollection,
    achievement_collection: AchievementCollection,
    motor_session: AsyncIOMotorClientSession,
) -> MongoDBUnitOfWork:
    return MongoDBUnitOfWork(
        commit_user_collection_changes=(
            CommitUserCollectionChanges(user_collection)
        ),
        commit_movie_collection_changes=(
            CommitMovieCollectionChanges(movie_collection)
        ),
        commit_person_collection_changes=(
            CommitPersonCollectionChanges(person_collection)
        ),
        commit_role_collection_changes=(
            CommitRoleCollectionChanges(role_collection)
        ),
        commit_writer_collection_changes=(
            CommitWriterCollectionChanges(writer_collection)
        ),
        commit_crew_member_collection_changes=(
            CommitCrewMemberCollectionChanges(crew_member_collection)
        ),
        commit_add_movie_contribution_collection_changes=(
            CommitAddMovieContributionCollectionChanges(
                add_movie_contribution_collection,
            )
        ),
        commit_edit_movie_contribution_collection_changes=(
            CommitEditMovieContributionCollectionChanges(
                edit_movie_contribution_collection,
            )
        ),
        commit_add_person_contribution_collection_changes=(
            CommitAddPersonContributionCollectionChanges(
                add_person_contribution_collection,
            )
        ),
        commit_edit_person_contribution_collection_changes=(
            CommitEditPersonContributionCollectionChanges(
                edit_person_contribution_collection,
            )
        ),
        commit_achievement_collection_changes=(
            CommitAchievementCollectionChanges(achievement_collection)
        ),
        session=motor_session,
    )


@pytest.fixture
def user_gateway(
    user_collection: UserCollection,
    unit_of_work: MongoDBUnitOfWork,
) -> UserMapper:
    return UserMapper(
        user_map=UserMap(),
        user_collection=user_collection,
        lock_factory=MongoDBLockFactory(),
        unit_of_work=unit_of_work,
    )


@pytest.fixture
def movie_gateway(
    movie_collection: MovieCollection,
    unit_of_work: MongoDBUnitOfWork,
) -> MovieMapper:
    return MovieMapper(
        movie_map=MovieMap(),
        movie_collection=movie_collection,
        lock_factory=MongoDBLockFactory(),
        unit_of_work=unit_of_work,
    )


@pytest.fixture
def person_gateway(
    person_collection: PersonCollection,
    unit_of_work: MongoDBUnitOfWork,
) -> PersonMapper:
    return PersonMapper(
        person_map=PersonMap(),
        person_collection=person_collection,
        lock_factory=MongoDBLockFactory(),
        unit_of_work=unit_of_work,
    )


@pytest.fixture
def role_gateway(
    role_collection: RoleCollection,
    unit_of_work: MongoDBUnitOfWork,
) -> RoleMapper:
    return RoleMapper(
        role_map=RoleMap(),
        role_collection=role_collection,
        unit_of_work=unit_of_work,
    )


@pytest.fixture
def writer_gateway(
    writer_collection: WriterCollection,
    unit_of_work: MongoDBUnitOfWork,
) -> WriterMapper:
    return WriterMapper(
        writer_map=WriterMap(),
        writer_collection=writer_collection,
        unit_of_work=unit_of_work,
    )


@pytest.fixture
def crew_member_gateway(
    crew_member_collection: CrewMemberCollection,
    unit_of_work: MongoDBUnitOfWork,
) -> CrewMemberMapper:
    return CrewMemberMapper(
        crew_member_map=CrewMemberMap(),
        crew_member_collection=crew_member_collection,
        unit_of_work=unit_of_work,
    )


@pytest.fixture
def add_movie_contribution_gateway(
    add_movie_contribution_collection: AddMovieContributionCollection,
    unit_of_work: MongoDBUnitOfWork,
) -> AddMovieContributionMapper:
    return AddMovieContributionMapper(
        contribution_map=AddMovieContributionMap(),
        contribution_collection=add_movie_contribution_collection,
        lock_factory=MongoDBLockFactory(),
        unit_of_work=unit_of_work,
    )


@pytest.fixture
def edit_movie_contribution_gateway(
    edit_movie_contribution_collection: EditMovieContributionCollection,
    unit_of_work: MongoDBUnitOfWork,
) -> EditMovieContributionMapper:
    return EditMovieContributionMapper(
        contribution_map=EditMovieContributionMap(),
        contribution_collection=edit_movie_contribution_collection,
        lock_factory=MongoDBLockFactory(),
        unit_of_work=unit_of_work,
    )


@pytest.fixture
def add_person_contribution_gateway(
    add_person_contribution_collection: AddPersonContributionCollection,
    unit_of_work: MongoDBUnitOfWork,
) -> AddPersonContributionMapper:
    return AddPersonContributionMapper(
        contribution_map=AddPersonContributionMap(),
        contribution_collection=add_person_contribution_collection,
        lock_factory=MongoDBLockFactory(),
        unit_of_work=unit_of_work,
    )


@pytest.fixture
def edit_person_contribution_gateway(
    edit_person_contribution_collection: EditPersonContributionCollection,
    unit_of_work: MongoDBUnitOfWork,
) -> EditPersonContributionMapper:
    return EditPersonContributionMapper(
        contribution_map=EditPersonContributionMap(),
        contribution_collection=(edit_person_contribution_collection),
        lock_factory=MongoDBLockFactory(),
        unit_of_work=unit_of_work,
    )


@pytest.fixture
def achievement_gateway(
    achievement_collection: AchievementCollection,
    unit_of_work: MongoDBUnitOfWork,
) -> AchievementMapper:
    return AchievementMapper(
        achievement_map=AchievementMap(),
        achievement_collection=achievement_collection,
        unit_of_work=unit_of_work,
    )


@pytest.fixture
def permissions_storage(
    permissions_collection: PermissionsCollection,
    motor_session: AsyncIOMotorClientSession,
    redis_client: Redis,
) -> PermissionsStorage:
    permissions_mapper = PermissionsMapper(
        permissions_collection=permissions_collection,
        session=motor_session,
    )
    permissions_cache = PermissionsCache(redis_client)
    permissions_storage = PermissionsStorage(
        permissions_mapper=permissions_mapper,
        permissions_cache=permissions_cache,
    )

    return permissions_storage
