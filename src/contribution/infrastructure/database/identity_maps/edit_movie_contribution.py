from typing import Optional

from contribution.domain import (
    EditMovieContributionId,
    EditMovieContribution,
)


class EditMovieContributionMap:
    def __init__(self):
        self._contributions: set[EditMovieContribution] = set()

    def with_id(
        self,
        id: EditMovieContributionId,
    ) -> Optional[EditMovieContribution]:
        for contribution in self._contributions:
            if contribution.id == id:
                return contribution
        return None

    def save(self, contribution: EditMovieContribution) -> None:
        """
        Saves contribution in identity map if contribution doesn't
        exist, otherwise raises ValueError.
        """
        contribution_from_map = self.with_id(contribution.id)
        if contribution_from_map:
            message = "Edit movie contribution already exists in identity map"
            raise ValueError(message)
        self._contributions.add(contribution)
