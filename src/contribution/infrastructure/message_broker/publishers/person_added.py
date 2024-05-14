# mypy: disable-error-code="assignment"

import json

from aio_pika import Exchange, Message

from contribution.application.common.events import PersonAddedEvent


class PublishPersonAddedEvent:
    def __init__(
        self,
        exchange: Exchange,
        routing_key: str,
    ):
        self._exchange = exchange
        self._routing_key = routing_key

    async def __call__(self, event: PersonAddedEvent) -> None:
        message_body_as_dict = {
            "contribution_id": str(event.contribtion_id),
            "author_id": str(event.author_id),
            "first_name": event.first_name,
            "last_name": event.last_name,
            "sex": event.sex.value,
            "birt_date": event.birth_date.isoformat(),
            "photos": list(event.photos),
            "added_at": event.added_at.isoformat(),
        }

        if event.death_date:
            message_body_as_dict["death_date"] = event.death_date.isoformat()
        else:
            message_body_as_dict["death_date"] = None

        message_body = json.dumps(message_body_as_dict).encode()

        await self._exchange.publish(
            message=Message(message_body),
            routing_key=self._routing_key,
        )
