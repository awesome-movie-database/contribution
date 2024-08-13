from faststream import FastStream
from dishka.integrations.faststream import setup_dishka

from contribution.infrastructure import rabbitmq_config_from_env
from contribution.infrastructure.di.event_consumer import (
    event_consumer_ioc_container_factory,
)
from contribution.presentation.event_consumer import create_broker


def create_event_consumer_app() -> FastStream:
    rabbitmq_config = rabbitmq_config_from_env()
    broker = create_broker(rabbitmq_config.url)

    app = FastStream(
        broker=broker,
        title="Contribution",
        version="0.1.0",
    )
    ioc_container = event_consumer_ioc_container_factory()
    setup_dishka(ioc_container, app)

    return app
