from dataclasses import dataclass
from typing import Optional

from contribution.domain import (
    EditMovieContributionId,
    EditMovieContribution,
)


@dataclass(slots=True, unsafe_hash=True)
class EditMovieContributionMapUnit:
    contribution: EditMovieContribution
    is_acquired: bool


class EditMovieContributionMap:
    def __init__(self):
        self._units: set[EditMovieContributionMapUnit] = set()

    def with_id(
        self,
        id: EditMovieContributionId,
    ) -> Optional[EditMovieContribution]:
        for unit in self._units:
            if unit.contribution.id == id:
                return unit.contribution
        return None

    def save(self, contribution: EditMovieContribution) -> None:
        """
        Saves contribution in identity map if contribution doesn't
        exist, otherwise raises ValueError.
        """
        contribution_from_map = self.with_id(contribution.id)
        if contribution_from_map:
            message = "Add movie contribution already exists in identity map"
            raise ValueError(message)

        unit = EditMovieContributionMapUnit(
            contribution=contribution,
            is_acquired=False,
        )
        self._units.add(unit)

    def save_acquired(self, contribution: EditMovieContribution) -> None:
        """
        Saves contribution as acquired in identity map if contribution
        doesn't exist or already exist and not marked as
        acquired, otherwise raises ValueError.
        """
        contribution_from_map = self.with_id(contribution.id)
        if not contribution_from_map:
            unit = EditMovieContributionMapUnit(
                contribution=contribution,
                is_acquired=True,
            )
            self._units.add(unit)

        contribution_is_acquired = self.is_acquired(contribution)
        if contribution_is_acquired:
            message = (
                "EditMovieContribution already exists in identity map"
                "and marked as acquired"
            )
            raise ValueError(message)

        for unit in self._units:
            if unit.contribution == contribution:
                unit.is_acquired = True
                return

    def is_acquired(self, contribution: EditMovieContribution) -> bool:
        """
        Returns whether contribution is acquired if contribution exists
        in identity map, otherwise raises ValueError.
        """
        for unit in self._units:
            if unit.contribution == contribution:
                return unit.is_acquired
        message = "EditMovieContribution doesn't exist in identity map"
        raise ValueError(message)
