"""Misc utilities."""

import regex
import inflect

INFLECT = inflect.engine()
ORDINALS = [INFLECT.ordinal(x) for x in range(21)]
ORDINALS += [INFLECT.number_to_words(x) for x in ORDINALS]
WORD_TO_NUM = {INFLECT.number_to_words(x): x for x in range(21)}
NUM_WORDS = list(WORD_TO_NUM.keys())


FLAGS = regex.VERBOSE | regex.IGNORECASE


class DotDict(dict):
    """Allow dot.notation access to dictionary items"""
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


def squash(values):
    """Squash a list to a single value is its length is one."""
    return values if len(values) != 1 else values[0]


def as_list(values):
    """Convert values to a list."""
    return values if isinstance(values, (list, tuple, set)) else [values]


def to_float(value):
    """Convert the value to a float."""
    value = regex.sub(r'[^\d.]', '', value) if value else ''
    try:
        return float(value)
    except ValueError:
        return None


def to_int(value):
    """Convert value to an integer, handle 'no' or 'none' etc."""
    digits = regex.sub(r'\D', '', value) if value else ''
    try:
        return int(digits)
    except ValueError:
        value = value if value else ''
        return WORD_TO_NUM.get(value.lower().strip(), 0)
