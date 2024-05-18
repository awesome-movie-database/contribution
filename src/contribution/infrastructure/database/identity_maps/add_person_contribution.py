from typing import Optional

from contribution.domain import (
    AddPersonContributionId,
    AddPersonContribution,
)


class AddPersonContributionMap:
    def __init__(self):
        self._contributions: set[AddPersonContribution] = set()

    def with_id(
        self,
        id: AddPersonContributionId,
    ) -> Optional[AddPersonContribution]:
        for contribution in self._contributions:
            if contribution.id == id:
                return contribution
        return None

    def save(self, contribution: AddPersonContribution) -> None:
        """
        Saves contribution in identity map if contribution doesn't
        exist, otherwise raises ValueError.
        """
        contribution_from_map = self.with_id(contribution.id)
        if contribution_from_map:
            message = "Add person contribution already exists in identity map"
            raise ValueError(message)
        self._contributions.add(contribution)
