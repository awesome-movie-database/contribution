# mypy: disable-error-code="assignment"

import json
from typing import Optional, Sequence
from datetime import date, datetime

from aio_pika import Exchange, Message

from contribution.domain.constants import Sex
from contribution.domain.value_objects import (
    EditPersonContributionId,
    UserId,
    PersonId,
    PhotoUrl,
)
from contribution.domain.maybe import Maybe


class PublishPersonEditedEvent:
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
        id: EditPersonContributionId,
        author_id: UserId,
        person_id: PersonId,
        first_name: Maybe[str],
        last_name: Maybe[str],
        sex: Maybe[Sex],
        birth_date: Maybe[date],
        death_date: Maybe[Optional[date]],
        add_photos: Sequence[PhotoUrl],
        edited_at: datetime,
    ) -> None:
        message_body_as_dict = {
            "contribution_id": str(id),
            "author_id": str(author_id),
            "person_id": str(person_id),
            "add_photos": list(add_photos),
            "edited_at": edited_at.isoformat(),
        }

        if first_name.is_set:
            message_body_as_dict["first_name"] = first_name.value
        if last_name.is_set:
            message_body_as_dict["last_name"] = last_name.value
        if sex.is_set:
            message_body_as_dict["sex"] = sex.value.value
        if birth_date.is_set:
            message_body_as_dict["birth_date"] = birth_date.value.isoformat()

        if death_date.is_set:
            death_date_value = death_date.value

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
