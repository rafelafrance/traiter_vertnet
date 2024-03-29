"""Utilities for parsing numeric traits."""
from fractions import Fraction

import regex
from traiter.pylib.util import to_positive_float, to_positive_int

from vertnet.pylib.convert_units import convert_units
from vertnet.pylib.trait import Trait

from .util import RE_FLAGS, as_list, squash

LOOK_BACK_FAR = 40

QUOTES_VS_INCHES = regex.compile(r' \d " (?! \s* \} )', RE_FLAGS)
IS_COLLECTOR = regex.compile(r" collector ", RE_FLAGS)


def as_value(token, trait, value_field="number", unit_field="units"):
    """Convert token values and units to trait fields."""
    units = as_list(token.group.get(unit_field, []))
    trait.units = squash(units) if units else None
    values = []
    for i, val in enumerate(as_list(token.group.get(value_field, []))):
        val = to_positive_float(val)
        if val is None:
            return False
        unit = units[i] if i < len(units) else units[-1] if units else None
        values.append(convert_units(val, unit))
    if not values:
        return False
    trait.value = squash(values)
    trait.units_inferred = not bool(trait.units)
    return True


def add_flags(token, trait):
    """Add common flags to the numeric trait."""
    trait.is_flag_in_token(token, "ambiguous_key")
    trait.is_flag_in_token(token, "estimated_value")
    trait.is_value_in_token(token, "measured_from1", rename="measured_from")
    trait.is_value_in_token(token, "measured_from2", rename="measured_from")
    trait.is_value_in_token(token, "includes")
    trait.is_flag_in_token(token, "quest", rename="uncertain")


def simple(token, value="number", units="units"):
    """Handle a normal measurement notation."""
    trait = Trait(start=token.start, end=token.end)
    flag = as_value(token, trait, value, units)
    add_flags(token, trait)
    return trait if flag else None


def simple_len(token, value="number", units="len_units"):
    """Handle a normal mass notation."""
    return simple(token, value, units)


def simple_mass(token, value="number", units="mass_units"):
    """Handle a normal mass notation."""
    return simple(token, value, units)


def compound(token):
    """Handle a pattern like: 4 ft 9 in."""
    trait = Trait(start=token.start, end=token.end)
    trait.units = [token.group["feet"], token.group["inches"]]
    trait.units_inferred = False
    trait.is_flag_missing(token, "key", rename="ambiguous_key")
    fts = convert_units(to_positive_float(token.group["ft"]), "ft")
    ins = [
        convert_units(to_positive_float(i), "in") for i in as_list(token.group["in"])
    ]
    value = [round(fts + i, 2) for i in ins]
    trait.value = squash(value)
    add_flags(token, trait)
    return trait


def fraction(token):
    """Handle fractional values like 10 3/8 inches."""
    trait = Trait(start=token.start, end=token.end)
    trait.units = token.group.get("units")
    trait.units_inferred = not bool(trait.units)
    whole = to_positive_float(token.group.get("whole", "0"))
    numerator = to_positive_int(token.group["numerator"])
    denominator = to_positive_int(token.group["denominator"])
    try:
        trait.value = whole + Fraction(numerator, denominator)
    except TypeError:
        print(f"Fraction error: {numerator} / {denominator}")
        return None
    if trait.units:
        trait.value = convert_units(trait.value, trait.units)
    add_flags(token, trait)
    return trait


def shorthand_length(token, measurement=""):
    """Handle shorthand length notation like 11-22-33-44:55g."""
    trait = Trait(start=token.start, end=token.end)
    trait.value = to_positive_float(token.group.get(measurement))
    if not trait.value:
        return None
    trait.units = "mm_shorthand"
    trait.units_inferred = False
    trait.is_shorthand = True
    flag = measurement.split("_")[1]
    flag = f"estimated_{flag}"
    trait.is_flag_in_token(token, flag, rename="estimated_value")
    return trait


def numeric_fix_ups(trait, text):
    """All of the numeric fix-ups."""
    return fix_up_shorthand(trait, text) and fix_up_inches(trait, text)


def fix_up_shorthand(trait, text):
    """All of the fix-ups for numbers."""
    if not trait.is_shorthand:
        return trait
    start = max(0, trait.start - LOOK_BACK_FAR)
    if IS_COLLECTOR.search(text, start, trait.start):
        return None
    return trait


def fix_up_inches(trait, text):
    """Disambiguate between double quotes "3" and inch units 3"."""
    if (
        not trait.units
        and QUOTES_VS_INCHES.match(text[trait.end - 1 :])
        and text[trait.start : trait.end].count('"') == 0
    ):
        trait.end += 1
        trait.units = '"'
        trait.units_inferred = False
        trait.value = convert_units(trait.value, trait.units)
    return trait
