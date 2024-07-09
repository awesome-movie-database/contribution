import json

from aio_pika import Exchange, Message

from contribution.application import OperationId, AchievementEarnedEvent


async def publish_achievement_earned_event_factory(
    exchange: Exchange,
    operation_id: OperationId,
) -> "PublishAchievementEarnedEvent":
    return PublishAchievementEarnedEvent(
        exchange=exchange,
        routing_key="contribution.achievement_earned",
        operation_id=operation_id,
    )


class PublishAchievementEarnedEvent:
    def __init__(
        self,
        exchange: Exchange,
        routing_key: str,
        operation_id: OperationId,
    ):
        self._exchange = exchange
        self._routing_key = routing_key
        self._operation_id = operation_id

    async def __call__(self, event: AchievementEarnedEvent) -> None:
        await self._exchange.publish(
            message=Message(self._event_to_json(event).encode()),
            routing_key=self._routing_key,
        )

    def _event_to_json(self, event: AchievementEarnedEvent) -> str:
        event_as_dict = {
            "operation_id": self._operation_id.hex,
            "achievement_id": event.achievement_id.hex,
            "user_id": event.user_id.hex,
            "achieved": event.achieved,
            "achieved_at": event.achieved_at.isoformat(),
        }
        return json.dumps(event_as_dict)
