from typing import Optional

from contribution.domain import (
    AddMovieContributionId,
    AddMovieContribution,
)


class AddMovieContributionMap:
    def __init__(self):
        self._contributions: set[AddMovieContribution] = set()

    def with_id(
        self,
        id: AddMovieContributionId,
    ) -> Optional[AddMovieContribution]:
        for contribution in self._contributions:
            if contribution.id == id:
                return contribution
        return None

    def save(self, contribution: AddMovieContribution) -> None:
        """
        Saves contribution in identity map if contribution doesn't
        exist, otherwise raises ValueError.
        """
        contribution_from_map = self.with_id(contribution.id)
        if contribution_from_map:
            message = "Add movie contribution already exists in identity map"
            raise ValueError(message)
        self._contributions.add(contribution)
