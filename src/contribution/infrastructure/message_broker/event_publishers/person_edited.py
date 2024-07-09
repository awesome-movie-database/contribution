# mypy: disable-error-code="assignment"

import json

from aio_pika import Exchange, Message

from contribution.application import OperationId, PersonEditedEvent


def publish_person_edited_event_factory(
    exchange: Exchange,
    operation_id: OperationId,
) -> "PublishPersonEditedEvent":
    return PublishPersonEditedEvent(
        exchange=exchange,
        routing_key="contribution.person_edited",
        operation_id=operation_id,
    )


class PublishPersonEditedEvent:
    def __init__(
        self,
        exchange: Exchange,
        routing_key: str,
        operation_id: OperationId,
    ):
        self._exchange = exchange
        self._routing_key = routing_key
        self._operation_id = operation_id

    async def __call__(self, event: PersonEditedEvent) -> None:
        await self._exchange.publish(
            message=Message(self._event_to_json(event).encode()),
            routing_key=self._routing_key,
        )

    def _event_to_json(self, event: PersonEditedEvent) -> str:
        event_as_dict = {
            "operation_id": self._operation_id.hex,
            "contribution_id": event.contribution_id.hex,
            "author_id": event.author_id.hex,
            "person_id": event.person_id.hex,
            "add_photos": list(event.add_photos),
            "edited_at": event.edited_at.isoformat(),
        }

        if event.first_name.is_set:
            event_as_dict["first_name"] = event.first_name.value
        if event.last_name.is_set:
            event_as_dict["last_name"] = event.last_name.value
        if event.sex.is_set:
            event_as_dict["sex"] = event.sex.value
        if event.birth_date.is_set:
            event_as_dict["birth_date"] = event.birth_date.value.isoformat()
        if event.death_date.is_set:
            death_date = event.death_date
            if death_date:
                event_as_dict["death_date"] = death_date.value.isoformat()
            else:
                event_as_dict["death_date"] = None

        return json.dumps(event_as_dict)
