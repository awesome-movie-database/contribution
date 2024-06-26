__all__ = (
    "motor_client_factory",
    "motor_session_factory",
    "motor_database_factory",
)

from typing import AsyncGenerator

from motor.motor_asyncio import (
    AsyncIOMotorClient,
    AsyncIOMotorClientSession,
    AsyncIOMotorDatabase,
)

from .config import MongoDBConfig


def motor_client_factory(
    mongodb_config: MongoDBConfig,
) -> AsyncIOMotorClient:
    return AsyncIOMotorClient(
        host=mongodb_config.uri,
        port=mongodb_config.port,
    )


async def motor_session_factory(
    motor_client: AsyncIOMotorClient,
) -> AsyncGenerator[AsyncIOMotorClientSession, None]:
    session = await motor_client.start_session()
    try:
        async with session.start_transaction():  # type: ignore
            yield session
    finally:
        await session.end_session()


def motor_database_factory(
    motor_session: AsyncIOMotorClientSession,
) -> AsyncIOMotorDatabase:
    return motor_session.client.get_database("contribution")
