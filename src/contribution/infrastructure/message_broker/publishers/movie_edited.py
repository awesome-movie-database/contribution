# mypy: disable-error-code="assignment, misc"

import json

from aio_pika import Exchange, Message

from contribution.application import MovieEditedEvent


class PublishMovieEditedEvent:
    def __init__(
        self,
        exchange: Exchange,
        routing_key: str,
    ):
        self._exchange = exchange
        self._routing_key = routing_key

    async def __call__(self, event: MovieEditedEvent) -> None:
        message_body_as_dict = {
            "contribution_id": str(event.contribution_id),
            "author_id": str(event.author_id),
            "movie_id": str(event.movie_id),
            "add_photos": list(event.add_photos),
            "edited_at": event.edited_at.isoformat(),
        }

        if event.eng_title.is_set:
            message_body_as_dict["eng_title"] = event.eng_title.value
        if event.original_title.is_set:
            message_body_as_dict["original_title"] = event.original_title.value
        if event.release_date.is_set:
            message_body_as_dict["release_date"] = event.release_date.value
        if event.countries.is_set:
            message_body_as_dict["countries"] = event.countries.value
        if event.genres.is_set:
            message_body_as_dict["genres"] = [
                genre.value for genre in event.genres.value
            ]
        if event.mpaa.is_set:
            message_body_as_dict["mpaa"] = event.mpaa.value.value
        if event.duration.is_set:
            message_body_as_dict["duration"] = event.duration.value

        if event.budget.is_set:
            budget_value = event.budget.value

            if budget_value:
                message_body_as_dict["budget"] = {
                    "amount": budget_value.amount,
                    "currency": budget_value.currency,
                }
            else:
                message_body_as_dict["budget"] = None
        if event.revenue.is_set:
            revenue_value = event.revenue.value

            if revenue_value:
                message_body_as_dict["revenue"] = {
                    "amount": revenue_value.amount,
                    "currency": revenue_value.currency,
                }
            else:
                message_body_as_dict["revenue"] = None

        message_body_as_dict["add_roles"] = [
            {
                "person_id": str(role.person_id),
                "character": role.character,
                "importance": role.importance,
                "is_spoiler": role.is_spoiler,
            }
            for role in event.add_roles
        ]
        message_body_as_dict["remove_roles"] = [
            str(role_id) for role_id in event.remove_roles
        ]

        message_body_as_dict["add_writers"] = [
            {
                "person_id": str(writer.person_id),
                "writing": writer.writing.value,
            }
            for writer in event.add_writers
        ]
        message_body_as_dict["remove_writers"] = [
            str(writer_id) for writer_id in event.remove_writers
        ]

        message_body_as_dict["add_crew"] = [
            {
                "person_id": str(crew_member.person_id),
                "membership": crew_member.membership.value,
            }
            for crew_member in event.add_crew
        ]
        message_body_as_dict["remove_crew"] = [
            str(crew_member_id) for crew_member_id in event.remove_crew
        ]

        message_body = json.dumps(message_body_as_dict).encode()

        await self._exchange.publish(
            message=Message(message_body),
            routing_key=self._routing_key,
        )
