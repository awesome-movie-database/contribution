import json

from aio_pika import Exchange, Message

from contribution.application import AchievementEarnedEvent


class PublishAchievementEarnedEvent:
    def __init__(
        self,
        exchange: Exchange,
        routing_key: str,
    ):
        self._exchange = exchange
        self._routing_key = routing_key

    async def __call__(self, event: AchievementEarnedEvent) -> None:
        message_body_as_dict = (
            {
                "achievement_id": str(event.achievement_id),
                "user_id": str(event.user_id),
                "type": event.achieved.value,
                "achieved_at": event.achieved_at.isoformat(),
            },
        )
        message_body = json.dumps(message_body_as_dict).encode()

        await self._exchange.publish(
            message=Message(message_body),
            routing_key=self._routing_key,
        )
