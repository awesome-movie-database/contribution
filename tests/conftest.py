import os
from typing import AsyncGenerator

import pytest
from motor.motor_asyncio import (
    AsyncIOMotorClient,
    AsyncIOMotorClientSession,
    AsyncIOMotorDatabase,
)

from contribution.infrastructure import (
    MongoDBConfig,
    motor_client_factory,
    motor_session_factory,
    motor_database_factory,
    env_var_by_key,
)


@pytest.fixture
def motor_client() -> AsyncIOMotorClient:
    port_as_str = os.getenv("TEST_MONGODB_PORT")
    if port_as_str:
        port = int(port_as_str)
    else:
        port = None

    mongodb_config = MongoDBConfig(
        url=env_var_by_key("TEST_MONGODB_URL"),
        port=port,
    )
    motor_client = motor_client_factory(mongodb_config)

    return motor_client


@pytest.fixture
async def motor_session(
    motor_client: AsyncIOMotorClient,
) -> AsyncGenerator[AsyncIOMotorClientSession, None]:
    async for motor_session in motor_session_factory(motor_client):
        yield motor_session


@pytest.fixture
def motor_database(
    motor_session: AsyncIOMotorClientSession,
) -> AsyncIOMotorDatabase:
    return motor_database_factory(motor_session)


@pytest.fixture
async def clear_database(motor_database: AsyncIOMotorDatabase):
    collection_names = await motor_database.list_collection_names()
    for collection_name in collection_names:
        collection = motor_database.get_collection(collection_name)
        await collection.delete_many({})
