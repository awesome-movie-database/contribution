from dataclasses import dataclass
from typing import Optional

from contribution.domain import (
    AddMovieContributionId,
    AddMovieContribution,
)


@dataclass(slots=True)
class AddMovieContributionMapUnit:
    contribution: AddMovieContribution
    is_acquired: bool


class AddMovieContributionMap:
    def __init__(self):
        self._units: list[AddMovieContributionMapUnit] = list()

    def by_id(
        self,
        id: AddMovieContributionId,
    ) -> Optional[AddMovieContribution]:
        for unit in self._units:
            if unit.contribution.id == id:
                return unit.contribution
        return None

    def save(self, contribution: AddMovieContribution) -> None:
        """
        Saves contribution in identity map if contribution doesn't
        exist, otherwise raises ValueError.
        """
        contribution_from_map = self.by_id(contribution.id)
        if contribution_from_map:
            message = "Add movie contribution already exists in identity map"
            raise ValueError(message)

        unit = AddMovieContributionMapUnit(
            contribution=contribution,
            is_acquired=False,
        )
        self._units.append(unit)

    def save_acquired(self, contribution: AddMovieContribution) -> None:
        """
        Saves contribution as acquired in identity map if contribution
        doesn't exist or already exist and not marked as
        acquired, otherwise raises ValueError.
        """
        contribution_from_map = self.by_id(contribution.id)
        if not contribution_from_map:
            unit = AddMovieContributionMapUnit(
                contribution=contribution,
                is_acquired=True,
            )
            self._units.append(unit)
            return

        contribution_is_acquired = self.is_acquired(contribution)
        if contribution_is_acquired:
            message = (
                "AddMovieContribution already exists in identity map"
                "and marked as acquired"
            )
            raise ValueError(message)

        for unit in self._units:
            if unit.contribution == contribution:
                unit.is_acquired = True
                return

    def is_acquired(self, contribution: AddMovieContribution) -> bool:
        """
        Returns whether contribution is acquired if contribution exists
        in identity map, otherwise raises ValueError.
        """
        for unit in self._units:
            if unit.contribution == contribution:
                return unit.is_acquired
        message = "AddMovieContribution doesn't exist in identity map"
        raise ValueError(message)
