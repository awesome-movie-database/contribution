from faststream.rabbit import RabbitBroker

from .routers import admin_router


def create_broker(rabbitmq_url: str) -> RabbitBroker:
    broker = RabbitBroker(rabbitmq_url)

    broker.include_router(admin_router)

    return broker
