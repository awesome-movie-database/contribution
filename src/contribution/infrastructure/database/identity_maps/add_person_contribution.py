from dataclasses import dataclass
from typing import Optional

from contribution.domain import (
    AddPersonContributionId,
    AddPersonContribution,
)


@dataclass(slots=True)
class AddPersonContributionMapUnit:
    contribution: AddPersonContribution
    is_acquired: bool


class AddPersonContributionMap:
    def __init__(self):
        self._units: list[AddPersonContributionMapUnit] = list()

    def by_id(
        self,
        id: AddPersonContributionId,
    ) -> Optional[AddPersonContribution]:
        for unit in self._units:
            if unit.contribution.id == id:
                return unit.contribution
        return None

    def save(self, contribution: AddPersonContribution) -> None:
        """
        Saves contribution in identity map if contribution doesn't
        exist, otherwise raises Exception.
        """
        contribution_from_map = self.by_id(contribution.id)
        if contribution_from_map:
            message = "Add movie contribution already exists in identity map"
            raise Exception(message)

        unit = AddPersonContributionMapUnit(
            contribution=contribution,
            is_acquired=False,
        )
        self._units.append(unit)

    def save_acquired(self, contribution: AddPersonContribution) -> None:
        """
        Saves contribution as acquired in identity map if contribution
        doesn't exist or already exist and not marked as
        acquired, otherwise raises Exception.
        """
        contribution_from_map = self.by_id(contribution.id)
        if not contribution_from_map:
            unit = AddPersonContributionMapUnit(
                contribution=contribution,
                is_acquired=True,
            )
            self._units.append(unit)
            return

        contribution_is_acquired = self.is_acquired(contribution)
        if contribution_is_acquired:
            message = (
                "AddPersonContribution already exists in identity map"
                "and marked as acquired"
            )
            raise Exception(message)

        for unit in self._units:
            if unit.contribution == contribution:
                unit.is_acquired = True
                return

    def is_acquired(self, contribution: AddPersonContribution) -> bool:
        """
        Returns whether contribution is acquired if contribution exists
        in identity map, otherwise raises Exception.
        """
        for unit in self._units:
            if unit.contribution == contribution:
                return unit.is_acquired
        message = "AddPersonContribution doesn't exist in identity map"
        raise Exception(message)
