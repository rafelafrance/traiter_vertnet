"""Misc utilities."""
import os
from contextlib import contextmanager
from pathlib import Path
from shutil import rmtree
from tempfile import mkdtemp
from typing import Any
from typing import Generator
from typing import Hashable
from typing import Optional
from typing import Union

import inflect
import regex
import regex as re

INFLECT = inflect.engine()
ORDINALS = [INFLECT.ordinal(x) for x in range(21)]
ORDINALS += [INFLECT.number_to_words(x) for x in ORDINALS]
WORD_TO_NUM = {INFLECT.number_to_words(x): x for x in range(21)}
NUM_WORDS = list(WORD_TO_NUM.keys())

RE_FLAGS = regex.VERBOSE | regex.IGNORECASE


class DotDict(dict):
    """Allow dot.notation access to dictionary items."""

    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


def to_positive_int(value):
    """Convert value to an integer, handle 'no' or 'none' etc."""
    digits = regex.sub(r"\D", "", value) if value else ""
    try:
        return int(digits)
    except ValueError:
        value = value if value else ""
        return WORD_TO_NUM.get(value.lower().strip(), 0)


@contextmanager
def get_temp_dir(
    prefix: str = "temp_", where: Optional[Union[str, Path]] = None, keep: bool = False
) -> Generator:
    """Handle creation and deletion of temporary directory."""
    if where and not os.path.exists(where):
        os.mkdir(where)

    temp_dir = mkdtemp(prefix=prefix, dir=where)

    try:
        yield temp_dir
    finally:
        if not keep or not where:
            rmtree(temp_dir)


def flatten(nested: Any) -> list:
    """Flatten an arbitrarily nested list."""
    flat = []
    nested = nested if isinstance(nested, (list, tuple, set)) else [nested]
    for item in nested:
        # if not isinstance(item, str) and hasattr(item, '__iter__'):
        if isinstance(item, (list, tuple, set)):
            flat.extend(flatten(item))
        else:
            flat.append(item)
    return flat


def squash(values: Union[list, set]) -> Any:
    """Squash a list to a single value if its length is one."""
    return list(values) if len(values) != 1 else values[0]


def as_list(values: Any) -> list:
    """Convert values to a list."""
    return list(values) if isinstance(values, (list, tuple, set)) else [values]


def as_set(values: Any) -> set:
    """Convert values to a set."""
    return set(values) if isinstance(values, (list, tuple, set)) else {values}


def as_tuple(values: Any) -> tuple[Any, ...]:
    """Convert values to a tuple."""
    return tuple(values) if isinstance(values, (list, tuple, set)) else (values,)


def as_member(values: Any) -> Hashable:
    """Convert values to set members (hashable)."""
    return tuple(values) if isinstance(values, (list, set)) else values


def camel_to_snake(name: str) -> str:
    """Convert a camel case string to snake case."""
    split = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", split).lower()


def ordinal(i: str) -> str:
    """Convert the digit to an ordinal value: 1->1st, 2->2nd, etc."""
    return INFLECT.ordinal(i)


def number_to_words(number: str) -> str:
    """Convert the number or ordinal value into words."""
    return INFLECT.number_to_words(number)


def xor(one: Any, two: Any) -> bool:
    """Emulate a logical xor."""
    return (one and not two) or (not one and two)


def sign(x: Union[int, float]) -> int:
    """Return the sign of a number (-1, 0, 1)."""
    return 0 if x == 0 else (-1 if x < 0 else 1)
