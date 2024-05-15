# mypy: disable-error-code="assignment"

import json

from aio_pika import Exchange, Message

from contribution.application import MovieAddedEvent


class PublishMovieAddedEvent:
    def __init__(
        self,
        exchange: Exchange,
        routing_key: str,
    ):
        self._exchange = exchange
        self._routing_key = routing_key

    async def __call__(self, event: MovieAddedEvent) -> None:
        message_body_as_dict = {
            "contribution_id": str(event.contribution_id),
            "author_id": str(event.author_id),
            "eng_title": event.eng_title,
            "original_title": event.original_title,
            "release_date": event.release_date.isoformat(),
            "countries": event.countries,
            "genres": [genre.value for genre in event.genres],
            "mpaa": event.mpaa.value,
            "duration": event.duration,
            "photos": list(event.photos),
            "added_at": event.added_at.isoformat(),
        }

        if event.budget:
            message_body_as_dict["budget"] = {
                "amount": str(event.budget.amount),
                "currency": event.budget.currency,
            }
        else:
            message_body_as_dict["budget"] = None

        if event.revenue:
            message_body_as_dict["revenue"] = {
                "amount": str(event.revenue.amount),
                "currency": event.revenue.currency,
            }
        else:
            message_body_as_dict["revenue"] = None

        message_body_as_dict["roles"] = [
            {
                "person_id": str(role.person_id),
                "character": role.character,
                "importance": role.importance,
                "is_spoiler": role.is_spoiler,
            }
            for role in event.roles
        ]
        message_body_as_dict["writers"] = [
            {
                "person_id": str(writer.person_id),
                "writing": writer.writing.value,
            }
            for writer in event.writers
        ]
        message_body_as_dict["crew"] = [
            {
                "person_id": str(crew_member.person_id),
                "membership": crew_member.membership.value,
            }
            for crew_member in event.crew
        ]

        message_body = json.dumps(message_body_as_dict).encode()

        await self._exchange.publish(
            message=Message(message_body),
            routing_key=self._routing_key,
        )
