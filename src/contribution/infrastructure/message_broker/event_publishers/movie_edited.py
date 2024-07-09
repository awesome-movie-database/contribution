# mypy: disable-error-code="assignment"

import json

from aio_pika import Exchange, Message

from contribution.application import OperationId, MovieEditedEvent


def publish_movie_edited_event_factory(
    exchange: Exchange,
    operation_id: OperationId,
) -> "PublishMovieEditedEvent":
    return PublishMovieEditedEvent(
        exchange=exchange,
        routing_key="contribution.movie_edited",
        operation_id=operation_id,
    )


class PublishMovieEditedEvent:
    def __init__(
        self,
        exchange: Exchange,
        routing_key: str,
        operation_id: OperationId,
    ):
        self._exchange = exchange
        self._routing_key = routing_key
        self._operation_id = operation_id

    async def __call__(self, event: MovieEditedEvent) -> None:
        await self._exchange.publish(
            message=Message(self._event_to_json(event).encode()),
            routing_key=self._routing_key,
        )

    def _event_to_json(self, event: MovieEditedEvent) -> str:
        event_as_dict = {
            "operation_id": self._operation_id.hex,
            "contribution_id": event.contribution_id.hex,
            "author_id": event.author_id.hex,
            "movie_id": event.movie_id.hex,
            "remove_roles": [role_id.hex for role_id in event.remove_roles],
            "remove_writers": [
                writer_id.hex for writer_id in event.remove_writers
            ],
            "remove_crew": [
                crew_member_id.hex for crew_member_id in event.remove_crew
            ],
            "edited_at": event.edited_at.isoformat(),
        }

        roles_to_add_as_dicts = []
        for role_to_add in event.add_roles:
            role_as_dict = {
                "person_id": role_to_add.person_id.hex,
                "character": role_to_add.character,
                "importance": role_to_add.importance,
                "is_spoiler": role_to_add.is_spoiler,
            }
            roles_to_add_as_dicts.append(role_as_dict)
        event_as_dict["add_roles"] = roles_to_add_as_dicts

        writers_to_add_as_dicts = []
        for writer_to_add in event.add_writers:
            writer_as_dict = {
                "person_id": writer_to_add.person_id.hex,
                "writing": writer_to_add.writing,
            }
            writers_to_add_as_dicts.append(writer_as_dict)
        event_as_dict["add_writers"] = writers_to_add_as_dicts

        crew_to_add_as_dicts = []
        for crew_member_to_add in event.add_crew:
            crew_member_as_dict = {
                "person_id": crew_member_to_add.person_id.hex,
                "membership": crew_member_to_add.membership,
            }
            crew_to_add_as_dicts.append(crew_member_as_dict)
        event_as_dict["add_crew"] = crew_to_add_as_dicts

        if event.eng_title.is_set:
            event_as_dict["eng_title"] = event.eng_title.value
        if event.original_title.is_set:
            event_as_dict["original_title"] = event.original_title.value
        if event.release_date.is_set:
            event_as_dict[
                "release_date"
            ] = event.release_date.value.isoformat()
        if event.countries.is_set:
            event_as_dict["countries"] = list(event.countries.value)
        if event.genres.is_set:
            event_as_dict["genres"] = list(event.genres.value)
        if event.mpaa.is_set:
            event_as_dict["mpaa"] = event.mpaa.value
        if event.duration.is_set:
            event_as_dict["duration"] = event.duration.value
        if event.budget.is_set:
            budget = event.budget.value
            if budget:
                budget_as_dict = {
                    "amount": str(budget.amount),
                    "currency": budget.currency,
                }
            else:
                budget_as_dict = None
            event_as_dict["budget"] = budget_as_dict
        if event.revenue.is_set:
            revenue = event.revenue.value
            if revenue:
                revenue_as_dict = {
                    "amount": str(revenue.amount),
                    "currency": revenue.currency,
                }
            else:
                revenue_as_dict = None
            event_as_dict["revenue"] = revenue_as_dict

        return json.dumps(event_as_dict)
