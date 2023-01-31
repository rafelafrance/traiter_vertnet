"""Misc utilities."""
import inflect
import regex

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
