"""Misc utilities."""

import regex
import inflect

INFLECT = inflect.engine()

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


def ordinal(i):
    """Convert the digit to an ordinal value: 1->1st, 2->2nd, etc."""
    return INFLECT.ordinal(i)


def number_to_words(number):
    """Convert the number or ordinal value into words."""
    return INFLECT.number_to_words(number)


def to_float(value):
    """Convert the value to a float."""
    value = regex.sub(r'[^\d.]', '', value) if value else ''
    try:
        return float(value)
    except ValueError:
        return None


def to_int(value):
    """Convert value to an integer, handle 'no' or 'none' etc."""
    value = regex.sub(r'\D', '', value) if value else ''
    try:
        return int(value)
    except ValueError:
        return 0
