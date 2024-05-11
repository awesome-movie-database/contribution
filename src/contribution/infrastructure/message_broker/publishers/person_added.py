# mypy: disable-error-code="assignment"

import json
from typing import Optional, Sequence
from datetime import date, datetime

from aio_pika import Exchange, Message

from contribution.domain.constants import Sex
from contribution.domain.value_objects import (
    AddPersonContributionId,
    UserId,
    PhotoUrl,
)


class PublishPersonAddedEvent:
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
        id: AddPersonContributionId,
        author_id: UserId,
        first_name: str,
        last_name: str,
        sex: Sex,
        birth_date: date,
        death_date: Optional[date],
        photos: Sequence[PhotoUrl],
        added_at: datetime,
    ) -> None:
        message_body_as_dict = {
            "contribution_id": str(id),
            "author_id": str(author_id),
            "first_name": first_name,
            "last_name": last_name,
            "sex": sex.value,
            "birt_date": birth_date.isoformat(),
            "photos": list(photos),
            "added_at": added_at.isoformat(),
        }

        if death_date:
            message_body_as_dict["death_date"] = death_date.isoformat()
        else:
            message_body_as_dict["death_date"] = None

        message_body = json.dumps(message_body_as_dict).encode()

        await self._exchange.publish(
            message=Message(message_body),
            routing_key=self._routing_key,
        )
