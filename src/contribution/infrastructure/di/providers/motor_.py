from typing import AsyncGenerator

from dishka import Provider, Scope
from motor.motor_asyncio import (
    AsyncIOMotorClient,
    AsyncIOMotorClientSession,
    AsyncIOMotorDatabase,
)

from contribution.infrastructure.database import MongoDBConfig


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
    async with motor_client.start_session() as session:
        async with session.start_transaction():
            yield session


def database_factory(
    motor_session: AsyncIOMotorClientSession,
) -> AsyncIOMotorDatabase:
    return motor_session.client.get_database("contribution")


def motor_provider_factory() -> Provider:
    provider = Provider(Scope.REQUEST)

    provider.provide(motor_client_factory, scope=Scope.APP)
    provider.provide(motor_session_factory)
    provider.provide(database_factory)

    return provider
