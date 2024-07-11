import json

from aio_pika import Exchange, Message

from contribution.application import OperationId, MovieAddedEvent


def publish_movie_added_event_factory(
    exchange: Exchange,
    operation_id: OperationId,
) -> "PublishMovieAddedEvent":
    return PublishMovieAddedEvent(
        exchange=exchange,
        routing_key="contribution.movie_added",
        operation_id=operation_id,
    )


class PublishMovieAddedEvent:
    def __init__(
        self,
        exchange: Exchange,
        routing_key: str,
        operation_id: OperationId,
    ):
        self._exchange = exchange
        self._routing_key = routing_key
        self._operation_id = operation_id

    async def __call__(self, event: MovieAddedEvent) -> None:
        await self._exchange.publish(
            message=Message(self._event_to_json(event).encode()),
            routing_key=self._routing_key,
        )

    def _event_to_json(self, event: MovieAddedEvent) -> str:
        if event.budget:
            budget_as_dict = {
                "amount": str(event.budget.amount),
                "currency": event.budget.currency,
            }
        else:
            budget_as_dict = None

        if event.revenue:
            revenue_as_dict = {
                "amount": str(event.revenue.amount),
                "currency": event.revenue.currency,
            }
        else:
            revenue_as_dict = None

        roles_as_dicts = []
        for role in event.roles:
            role_as_dict = {
                "person_id": role.person_id.hex,
                "character": role.character,
                "importance": role.importance,
                "is_spoiler": role.is_spoiler,
            }
            roles_as_dicts.append(role_as_dict)

        writers_as_dicts = []
        for writer in event.writers:
            writer_as_dict = {
                "person_id": writer.person_id.hex,
                "writing": writer.writing,
            }
            writers_as_dicts.append(writer_as_dict)

        crew_as_dicts = []
        for crew_member in event.crew:
            crew_member_as_dict = {
                "person_id": crew_member.person_id.hex,
                "membership": crew_member.membership,
            }
            crew_as_dicts.append(crew_member_as_dict)

        event_as_dict = {
            "operation_id": self._operation_id,
            "contribution_id": event.contribution_id.hex,
            "author_id": event.author_id.hex,
            "eng_title": event.eng_title,
            "original_title": event.original_title,
            "release_date": event.release_date.isoformat(),
            "countries": list(event.countries),
            "genres": list(event.genres),
            "mpaa": event.mpaa,
            "duration": event.duration,
            "budget": budget_as_dict,
            "revenue": revenue_as_dict,
            "roles": roles_as_dicts,
            "writers": writers_as_dicts,
            "crew": crew_as_dicts,
            "photos": event.photos,
            "added_at": event.added_at.isoformat(),
        }
        return json.dumps(event_as_dict)
