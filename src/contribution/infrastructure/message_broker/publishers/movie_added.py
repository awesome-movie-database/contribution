# mypy: disable-error-code="assignment"

import json
from typing import Optional, Sequence
from datetime import date, datetime

from aio_pika import Exchange, Message

from contribution.domain.constants import (
    Genre,
    MPAA,
)
from contribution.domain.value_objects import (
    AddMovieContributionId,
    UserId,
    Country,
    Money,
    ContributionRole,
    ContributionWriter,
    ContributionCrewMember,
    PhotoUrl,
)


class PublishMovieAddedEvent:
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
        id: AddMovieContributionId,
        author_id: UserId,
        eng_title: str,
        original_title: str,
        release_date: date,
        countries: Sequence[Country],
        genres: Sequence[Genre],
        mpaa: MPAA,
        duration: int,
        budget: Optional[Money],
        revenue: Optional[Money],
        roles: Sequence[ContributionRole],
        writers: Sequence[ContributionWriter],
        crew: Sequence[ContributionCrewMember],
        photos: Sequence[PhotoUrl],
        added_at: datetime,
    ) -> None:
        message_body_as_dict = {
            "contribution_id": str(id),
            "author_id": str(author_id),
            "eng_title": eng_title,
            "original_title": original_title,
            "release_date": release_date.isoformat(),
            "countries": countries,
            "genres": [genre.value for genre in genres],
            "mpaa": mpaa.value,
            "duration": duration,
            "photos": list(photos),
            "added_at": added_at.isoformat(),
        }

        if budget:
            message_body_as_dict["budget"] = {
                "amount": str(budget.amount),
                "currency": budget.currency,
            }
        else:
            message_body_as_dict["budget"] = None

        if revenue:
            message_body_as_dict["revenue"] = {
                "amount": str(revenue.amount),
                "currency": revenue.currency,
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
            for role in roles
        ]
        message_body_as_dict["writers"] = [
            {
                "person_id": str(writer.person_id),
                "writing": writer.writing.value,
            }
            for writer in writers
        ]
        message_body_as_dict["crew"] = [
            {
                "person_id": str(crew_member.person_id),
                "membership": crew_member.membership.value,
            }
            for crew_member in crew
        ]

        message_body = json.dumps(message_body_as_dict).encode()

        await self._exchange.publish(
            message=Message(message_body),
            routing_key=self._routing_key,
        )
