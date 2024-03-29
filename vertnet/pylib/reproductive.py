"""Functions common to most male & female reproductive traits."""
from copy import copy
from string import punctuation

from traiter.pylib.old.rule import part
from traiter.pylib.old.token import Token

from vertnet.pylib.numeric import as_value
from vertnet.pylib.patterns import CROSS
from vertnet.pylib.trait import Trait

# Used to get compounds traits from a single parse
DOUBLE_CROSS = part(name="double_cross", regexp=f" {CROSS} ")

SIDES = {"l": "r", "r": "l", "left": "right", "right": "left", "lft": "rt", "rt": "lft"}


def double(token):
    """Convert a single token into multiple (two) parsers."""
    trait1 = Trait(start=token.start, end=token.end)
    token1 = Token(DOUBLE_CROSS, group=copy(token.group))
    token1.group["units"] = token.group.get("units_1")
    token1.group["value"] = token.group.get("value_1")
    side1 = token.group.get("side_1")

    trait2 = Trait(start=token.start, end=token.end)
    token2 = Token(DOUBLE_CROSS, group=copy(token.group))
    token2.group["units"] = token.group.get("units_2")
    token2.group["value"] = token.group.get("value_2")
    side2 = token.group.get("side_2")

    if token1.group["units"] and not token2.group["units"]:
        token2.group["units"] = token1.group["units"]
    elif token2.group["units"] and not token1.group["units"]:
        token1.group["units"] = token2.group["units"]

    flag1 = as_value(token1, trait1, value_field="value")
    flag2 = as_value(token2, trait2, value_field="value")
    if not flag1 or not flag2:
        return None

    side1 = side1.lower().strip(punctuation) if side1 else None
    side2 = side2.lower().strip(punctuation) if side2 else None
    side1 = side1 if side1 else SIDES.get(side2)
    side2 = side2 if side2 else SIDES.get(side1)

    if side1:
        trait1.side = side1
    if side2:
        trait2.side = side2

    return [trait1, trait2]


def convert(token):
    """Convert parsed token into a trait product."""
    trait = Trait(start=token.start, end=token.end)
    flag = as_value(token, trait, unit_field="len_units")

    trait.is_flag_in_token(token, "ambiguous_char", rename="ambiguous_key")
    trait.is_flag_in_token(token, "ambiguous_key")
    trait.is_value_in_token(token, "dimension")
    trait.is_value_in_token(token, "dim", rename="dimension")
    trait.is_value_in_token(token, "side")
    return trait if flag else None
