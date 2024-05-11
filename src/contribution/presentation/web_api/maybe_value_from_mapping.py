from typing import Mapping, TypeVar, get_type_hints

from contribution.domain.maybe import Maybe


_K = TypeVar("_K")
_V = TypeVar("_V")


def maybe_value_from_mapping(mapping: Mapping[_K, _V], key: _K) -> Maybe:
    """
    Returns wrapped in Maybe value from mapping by key
    if value exists in mapping, otherwise returns Maybe
    without value. Raises ValueError if mapping has no
    annotation for value retrieved by key.

    Basic usage::

        from typing import TypedDict

        class Foo(TypedDict, total=False):
            a: int
            b: str

        foo = Foo(a=10)

        a = maybe_value_from_mapping(foo, "a")
        print(a.is_set)  # True
        print(a.value)  # 10

        b = maybe_value_from_mapping(foo, "b")
        print(b.is_set)  # False
        print(b.value)  # Raises ValueError
    """
    value_type = get_type_hints(mapping).get(key)  # type: ignore
    if not value_type:
        message = f"Mapping has no type hints for key {key}"
        raise ValueError(message)

    value = mapping.get(key)
    if value:
        return Maybe.with_value(value)

    return Maybe.without_value()
