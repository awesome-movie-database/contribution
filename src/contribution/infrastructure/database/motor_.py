__all__ = (
    "motor_client_factory",
    "motor_session_factory",
    "motor_database_factory",
)

from typing import AsyncGenerator
from contextlib import asynccontextmanager

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
        host=mongodb_config.url,
        port=mongodb_config.port,
    )


@asynccontextmanager
async def motor_session_factory(
    motor_client: AsyncIOMotorClient,
) -> AsyncGenerator[AsyncIOMotorClientSession, None]:
    async with await motor_client.start_session() as motor_session:
        async with motor_session.start_transaction():
            yield motor_session


def motor_database_factory(
    motor_session: AsyncIOMotorClientSession,
) -> AsyncIOMotorDatabase:
    return motor_session.client.get_database("contribution")
