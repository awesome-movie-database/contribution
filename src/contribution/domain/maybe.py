from typing import TypeVar, Generic, Union, cast
from enum import IntEnum, auto


_T = TypeVar("_T")


class _Unset(IntEnum):
    UNSET = auto()


class Maybe(Generic[_T]):
    """
    Class for representing value that can be
    not set.

    Basic usage::

        class Foo:
            def __init__(self, bar: Optional[int]):
                self.bar = bar

        foo = Foo(1)

        def update_foo(bar: Maybe[Optional[int]]):
            if bar.is_set:
                foo.bar = bar
    """

    def __init__(self, value: Union[_T, _Unset]) -> None:
        self._value = value

    @classmethod
    def without_value(cls) -> "Maybe[_T]":
        return Maybe(_Unset.UNSET)

    @classmethod
    def with_value(cls, value: _T) -> "Maybe[_T]":
        return Maybe(value)

    @property
    def is_set(self) -> bool:
        return not isinstance(self._value, _Unset)

    @property
    def value(self) -> _T:
        """
        Returns value if value is set, otherwise
        raises ValueError.
        """
        if not self.is_set:
            message = "Value is unset"
            raise ValueError(message)
        return cast(_T, self.value)
