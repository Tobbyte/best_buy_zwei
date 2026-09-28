"""A module to validate fields of a class."""

from collections.abc import Callable
from functools import wraps
from typing import Any

from config import (
    VALIDATE_ERR_MUST_BE_POSITIVE,
    VALIDATE_ERR_NOT_OF_TYPE,
    VALIDATE_ERR_STR_EMPTY,
)


def validate(eval_fields: dict, *, no_negatives: bool = True) -> Callable:
    """Validate against eval_fields.

    Args:
        eval_fields (dict): A dic of field names and their expected
        types which are valid for that class.
        no_negatives (bool): If True, negative values are not allowed.

    Note:
    isinstance(value, expected_type) fails for parameterized generics,
    e.g. 'list[int]'. Won't fix, too much for this project.

    """

    def deco(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(self: Any, name: str, value: Any) -> None:  # noqa: ANN401
            """Validate."""
            expected_type = eval_fields.get(name)
            if expected_type and expected_type is str and not value:
                err_msg = VALIDATE_ERR_STR_EMPTY.format(name=name)
                raise TypeError(err_msg)

            if expected_type and not isinstance(value, expected_type):  # pyright: ignore[reportArgumentType]
                err_msg = VALIDATE_ERR_NOT_OF_TYPE.format(
                    name=name,
                    type=expected_type,
                )
                raise TypeError(err_msg)

            if (
                expected_type
                and isinstance(value, (int | float))
                and no_negatives
                and value < 0
            ):
                err_msg = VALIDATE_ERR_MUST_BE_POSITIVE.format(name=name)
                raise TypeError(err_msg)

            func(self, name, value)

        return wrapper

    return deco
