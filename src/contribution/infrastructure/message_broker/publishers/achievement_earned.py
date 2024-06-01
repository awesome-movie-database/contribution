from aio_pika import Exchange, Message

from contribution.infrastructure.message_broker.outcoming_events import (
    OutcomingAchievementEarnedEvent,
)


class PublishAchievementEarnedEvent:
    def __init__(
        self,
        exchange: Exchange,
        routing_key: str,
    ):
        self._exchange = exchange
        self._routing_key = routing_key

    async def __call__(self, event: OutcomingAchievementEarnedEvent) -> None:
        await self._exchange.publish(
            message=Message(event.to_json().encode()),
            routing_key=self._routing_key,
        )
