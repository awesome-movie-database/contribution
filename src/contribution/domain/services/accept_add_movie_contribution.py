from datetime import datetime

from contribution.domain.constants import ContributionStatus
from contribution.domain.entities import (
    AddMovieContribution,
    User,
)


class AcceptAddMovieContribution:
    def __init__(self, increase_rating_on: float):
        self._increase_rating_on = increase_rating_on

    def __call__(
        self,
        *,
        add_movie_contribution: AddMovieContribution,
        author: User,
        current_timestamp: datetime,
    ) -> None:
        add_movie_contribution.status = ContributionStatus.ACCEPTED
        add_movie_contribution.updated_at = current_timestamp

        author.rating += self._increase_rating_on
        author.contributions_count += 1
