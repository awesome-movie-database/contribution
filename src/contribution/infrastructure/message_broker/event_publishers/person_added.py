import json

from aio_pika import Exchange, Message

from contribution.application import OperationId, PersonAddedEvent


def publish_person_added_event_factory(
    exchange: Exchange,
    operation_id: OperationId,
) -> "PublishPersonAddedEvent":
    return PublishPersonAddedEvent(
        exchange=exchange,
        routing_key="contribution.person_added",
        operation_id=operation_id,
    )


class PublishPersonAddedEvent:
    def __init__(
        self,
        exchange: Exchange,
        routing_key: str,
        operation_id: OperationId,
    ):
        self._exchange = exchange
        self._routing_key = routing_key
        self._operation_id = operation_id

    async def __call__(self, event: PersonAddedEvent) -> None:
        await self._exchange.publish(
            message=Message(self._event_to_json(event).encode()),
            routing_key=self._routing_key,
        )

    def _event_to_json(self, event: PersonAddedEvent) -> str:
        if event.death_date:
            death_date = event.death_date.isoformat()
        else:
            death_date = None

        event_as_dict = {
            "operation_id": self._operation_id,
            "contribution_id": event.contribtion_id,
            "author_id": event.author_id,
            "first_name": event.first_name,
            "last_name": event.last_name,
            "sex": event.sex,
            "birth_date": event.birth_date.isoformat(),
            "death_date": death_date,
            "photos": list(event.photos),
            "added_at": event.added_at.isoformat(),
        }
        return json.dumps(event_as_dict)
