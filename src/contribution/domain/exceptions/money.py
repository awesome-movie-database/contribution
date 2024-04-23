__all__ = (
    "MoneyCurrenciesDoesNotMatchError",
    "MoneyAmountLessThanZeroError",
)

from contribution.domain.value_objects import Currency


class MoneyCurrenciesDoesNotMatchError(Exception):
    def __init__(
        self,
        *,
        got: Currency,
        required: Currency,
    ) -> None:
        self._got = got
        self._required = required

    def __str__(self) -> str:
        return (
            "Currency doesn't match."
            f"Got {self._got}, but {self._required} is required."
        )


class MoneyAmountLessThanZeroError(Exception):
    ...
