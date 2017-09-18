from typing import Any

from hypothesis import (Verbosity,
                        find,
                        settings)
from hypothesis.searchstrategy import SearchStrategy


def example(strategy: SearchStrategy) -> Any:
    return find(specifier=strategy,
                condition=lambda x: True,
                settings=settings(max_shrinks=0,
                                  max_iterations=10000,
                                  database=None,
                                  verbosity=Verbosity.quiet))


def is_context_manager(object_: Any) -> bool:
    return (has_callable_attribute(object_,
                                   attribute='__enter__')
            and has_callable_attribute(object_,
                                       attribute='__exit__'))


def has_callable_attribute(object_: Any,
                           *,
                           attribute: str) -> bool:
    return callable(getattr(object_, attribute, None))


def is_non_empty_string(string: str) -> bool:
    return isinstance(string, str) and string
