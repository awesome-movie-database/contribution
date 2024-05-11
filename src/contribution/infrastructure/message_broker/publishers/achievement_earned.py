import json
from datetime import datetime

from aio_pika import Exchange, Message

from contribution.domain.constants import Achieved
from contribution.domain.value_objects import (
    UserId,
    AchievementId,
)


class PublishAchievementEarnedEvent:
    def __init__(
        self,
        exchange: Exchange,
        routing_key: str,
    ):
        self._exchange = exchange
        self._routing_key = routing_key

    async def __call__(
        self,
        *,
        id: AchievementId,
        user_id: UserId,
        achieved: Achieved,
        achieved_at: datetime,
    ) -> None:
        message_body_as_dict = (
            {
                "achievement_id": str(id),
                "user_id": str(user_id),
                "type": achieved.value,
                "achieved_at": achieved_at.isoformat(),
            },
        )
        message_body = json.dumps(message_body_as_dict).encode()

        await self._exchange.publish(
            message=Message(message_body),
            routing_key=self._routing_key,
        )
