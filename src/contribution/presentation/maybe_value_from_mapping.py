from typing import Mapping, Any

from contribution.domain.maybe import Maybe


def maybe_value_from_mapping[T](
    mapping: Mapping,
    key: Any,
) -> Maybe[T]:
    """
    Returns wrapped in Maybe value from mapping by key
    if value exists in mapping, otherwise returns Maybe
    without value.

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
    no_value = Maybe[T].without_value()

    value = mapping.get(key, no_value)
    if isinstance(value, Maybe):
        return value

    return Maybe[T].with_value(value)
