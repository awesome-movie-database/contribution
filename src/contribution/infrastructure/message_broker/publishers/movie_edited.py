# mypy: disable-error-code="assignment, misc"

import json
from typing import Optional, Sequence
from datetime import date, datetime

from aio_pika import Exchange, Message

from contribution.domain.constants import (
    Genre,
    MPAA,
)
from contribution.domain.value_objects import (
    EditMovieContributionId,
    UserId,
    MovieId,
    RoleId,
    WriterId,
    CrewMemberId,
    ContributionRole,
    ContributionWriter,
    ContributionCrewMember,
    Country,
    Money,
    PhotoUrl,
)
from contribution.domain.maybe import Maybe


class PublishMovieEditedEvent:
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
        id: EditMovieContributionId,
        author_id: UserId,
        movie_id: MovieId,
        eng_title: Maybe[str],
        original_title: Maybe[str],
        release_date: Maybe[date],
        countries: Maybe[Sequence[Country]],
        genres: Maybe[Sequence[Genre]],
        mpaa: Maybe[MPAA],
        duration: Maybe[int],
        budget: Maybe[Optional[Money]],
        revenue: Maybe[Optional[Money]],
        add_roles: Sequence[ContributionRole],
        remove_roles: Sequence[RoleId],
        add_writers: Sequence[ContributionWriter],
        remove_writers: Sequence[WriterId],
        add_crew: Sequence[ContributionCrewMember],
        remove_crew: Sequence[CrewMemberId],
        add_photos: Sequence[PhotoUrl],
        edited_at: datetime,
    ) -> None:
        message_body_as_dict = {
            "contribution_id": str(id),
            "author_id": str(author_id),
            "movie_id": str(movie_id),
            "add_photos": list(add_photos),
            "edited_at": edited_at.isoformat(),
        }

        if eng_title.is_set:
            message_body_as_dict["eng_title"] = eng_title.value
        if original_title.is_set:
            message_body_as_dict["original_title"] = original_title.value
        if release_date.is_set:
            message_body_as_dict["release_date"] = release_date.value
        if countries.is_set:
            message_body_as_dict["countries"] = countries.value
        if genres.is_set:
            message_body_as_dict["genres"] = [
                genre.value for genre in genres.value
            ]
        if mpaa.is_set:
            message_body_as_dict["mpaa"] = mpaa.value.value
        if duration.is_set:
            message_body_as_dict["duration"] = duration.value

        if budget.is_set:
            budget_value = budget.value

            if budget_value:
                message_body_as_dict["budget"] = {
                    "amount": budget_value.amount,
                    "currency": budget_value.currency,
                }
            else:
                message_body_as_dict["budget"] = None
        if revenue.is_set:
            revenue_value = revenue.value

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
            for role in add_roles
        ]
        message_body_as_dict["remove_roles"] = [
            str(role_id) for role_id in remove_roles
        ]

        message_body_as_dict["add_writers"] = [
            {
                "person_id": str(writer.person_id),
                "writing": writer.writing.value,
            }
            for writer in add_writers
        ]
        message_body_as_dict["remove_writers"] = [
            str(writer_id) for writer_id in remove_writers
        ]

        message_body_as_dict["add_crew"] = [
            {
                "person_id": str(crew_member.person_id),
                "membership": crew_member.membership.value,
            }
            for crew_member in add_crew
        ]
        message_body_as_dict["remove_crew"] = [
            str(crew_member_id) for crew_member_id in remove_crew
        ]

        message_body = json.dumps(message_body_as_dict).encode()

        await self._exchange.publish(
            message=Message(message_body),
            routing_key=self._routing_key,
        )
