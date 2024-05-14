# mypy: disable-error-code="assignment"

import json

from aio_pika import Exchange, Message

from contribution.application.common.events import PersonEditedEvent


class PublishPersonEditedEvent:
    def __init__(
        self,
        exchange: Exchange,
        routing_key: str,
    ):
        self._exchange = exchange
        self._routing_key = routing_key

    async def __call__(self, event: PersonEditedEvent) -> None:
        message_body_as_dict = {
            "contribution_id": str(event.contribution_id),
            "author_id": str(event.author_id),
            "person_id": str(event.person_id),
            "add_photos": list(event.add_photos),
            "edited_at": event.edited_at.isoformat(),
        }

        if event.first_name.is_set:
            message_body_as_dict["first_name"] = event.first_name.value
        if event.last_name.is_set:
            message_body_as_dict["last_name"] = event.last_name.value
        if event.sex.is_set:
            message_body_as_dict["sex"] = event.sex.value.value
        if event.birth_date.is_set:
            message_body_as_dict[
                "birth_date"
            ] = event.birth_date.value.isoformat()

        if event.death_date.is_set:
            death_date_value = event.death_date.value

            if death_date_value:
                message_body_as_dict[
                    "death_date"
                ] = death_date_value.isoformat()
            else:
                message_body_as_dict["death_date"] = None

        message_body = json.dumps(message_body_as_dict).encode()

        await self._exchange.publish(
            message=Message(message_body),
            routing_key=self._routing_key,
        )
