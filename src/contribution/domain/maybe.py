from typing import (
    Any,
    Callable,
    Mapping,
    Optional,
    Union,
    cast,
)
from enum import IntEnum, auto


class _Unset(IntEnum):
    UNSET = auto()


class Maybe[T]:
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

    def __init__(self, value: Union[T, _Unset]) -> None:
        self._value = value

    @classmethod
    def without_value(cls) -> "Maybe[T]":
        return Maybe(_Unset.UNSET)

    @classmethod
    def with_value(cls, value: T) -> "Maybe[T]":
        return Maybe(value)

    @classmethod
    def from_mapping_by_key(
        cls,
        mapping: Mapping,
        key: Any,
        *,
        value_factory: Optional[Callable[[Any], T]] = None,
    ) -> "Maybe[T]":
        """
        Returns value wrapped in Maybe from mapping
        by key if key exists, otherwise returns
        Maybe without value. Passes value from mapping
        to value factory if one was provided and wraps
        returned value in Maybe.

        Basic usage::

            @dataclass
            class Location:
                lat: float
                lng: float

            def mapping_to_location(mapping) -> Location:
                return Location(
                    lat=mapping.lat,
                    lng=mapping.lng,
                )

            foo = {
                "location": {
                    "lat": 10.5,
                    "lng": 10.5,
                },
            }
            bar = {}

            location_from_foo_dict = Maybe[Location].from_mapping_by_key(
                mapping=foo,
                key="location",
                value_factory=mapping_to_location,
            )
            print(location_from_foo_dict.is_set)  # True
            print(location_from_foo_dict.value)  # Location(lat=10.5, lng=10.5)

            location_from_bar_dict = Maybe[Location].from_mapping_by_key(
                mapping=bar,
                key="location",
                value_factory=mapping_to_location,
            )
            print(location_from_bar_dict.is_set)  # False
            print(location_from_bar_dict.value)  # Raises ValueError
        """
        value = mapping.get(key, Maybe[T].without_value())
        if isinstance(value, Maybe):
            return value

        if value_factory:
            value = value_factory(value)

        return Maybe[T].with_value(value)

    @property
    def is_set(self) -> bool:
        return not isinstance(self._value, _Unset)

    @property
    def value(self) -> T:
        """
        Returns value if value is set, otherwise
        raises ValueError.
        """
        if not self.is_set:
            message = "Value is unset"
            raise ValueError(message)
        return cast(T, self.value)
