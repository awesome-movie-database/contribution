from contextlib import asynccontextmanager
from typing import AsyncGenerator

from aio_pika import Connection, Channel, Exchange, connect_robust

from .config import RabbitMQConfig


@asynccontextmanager
async def aio_pika_connection_factory(
    rabbitmq_config: RabbitMQConfig,
) -> AsyncGenerator[Connection, None]:
    connection = await connect_robust(url=rabbitmq_config.url)
    try:
        yield connection
    finally:
        await connection.close()


@asynccontextmanager
async def aio_pika_channel_factory(
    aio_pika_connection: Connection,
) -> AsyncGenerator[Channel, None]:
    channel = await aio_pika_connection.channel()
    try:
        yield channel
    finally:
        await channel.close()


async def aio_pika_exchange_factory(
    aio_pika_channel: Channel,
) -> Exchange:
    return await aio_pika_channel.get_exchange("contribution")
