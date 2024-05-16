from typing import Iterable

from .base import DomainError


class ContributionDataDuplicationError(DomainError):
    def __init__(self, fields: Iterable[str]):
        self.fields = fields

    def __str__(self) -> str:
        return (
            "Contribution must not contain duplicate data from"
            "of the edited entity."
        )
