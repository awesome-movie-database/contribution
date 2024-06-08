from dataclasses import dataclass
from decimal import Decimal

from contribution.domain.exceptions import (
    MoneyCurrenciesDoNotMatchError,
    MoneyAmountLessThanZeroError,
)
from .currency import Currency


@dataclass(frozen=True, slots=True)
class Money:
    amount: Decimal
    currency: Currency

    def __post_init__(self) -> None:
        self._ensure_valid_amount()

    def __lt__(self, other_money: "Money") -> bool:
        self._ensure_currency_match(other_money.currency)
        return self.amount < other_money.amount

    def __le__(self, other_money: "Money") -> bool:
        self._ensure_currency_match(other_money.currency)
        return self.amount <= other_money.amount

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Money):
            return NotImplemented
        return self.amount == other.amount

    def __ne__(self, other: object) -> bool:
        return not self == other

    def __gt__(self, other_money: "Money") -> bool:
        self._ensure_currency_match(other_money.currency)
        return self.amount > other_money.amount

    def __ge__(self, other_money: "Money") -> bool:
        self._ensure_currency_match(other_money.currency)
        return self.amount >= other_money.amount

    def __add__(self, other_money: "Money") -> "Money":
        self._ensure_currency_match(other_money.currency)
        new_money = Money(
            amount=self.amount + other_money.amount,
            currency=self.currency,
        )
        return new_money

    def __sub__(self, other_money: "Money") -> "Money":
        self._ensure_currency_match(other_money.currency)
        new_money = Money(
            amount=self.amount - other_money.amount,
            currency=self.currency,
        )
        return new_money

    def _ensure_currency_match(self, currency: Currency) -> None:
        if currency != self.currency:
            raise MoneyCurrenciesDoNotMatchError(
                got=currency,
                required=self.currency,
            )

    def _ensure_valid_amount(self) -> None:
        if self.amount < 0:
            raise MoneyAmountLessThanZeroError()
