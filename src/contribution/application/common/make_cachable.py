from typing import Callable, cast
from functools import cache


def make_func_cacheable[F: Callable](func: F) -> F:
    return cast(F, cache(func))
