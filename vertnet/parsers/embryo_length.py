"""Parse embryo lengths."""

from traiter.old.vocabulary import Vocabulary
from traiter.util import as_list, to_positive_float

import vertnet.pylib.convert_units as convert_units
import vertnet.pylib.shared_reproductive_patterns as patterns
from vertnet.parsers.base import Base
from vertnet.pylib.numeric import add_flags, fix_up_inches, simple
from vertnet.pylib.trait import Trait

VOCAB = Vocabulary(patterns.VOCAB)

TOO_BIG = 1000


def convert(token):
    """Convert parsed token into a trait product."""
    trait = simple(token, units="len_units")
    return trait if all(x < TOO_BIG for x in as_list(trait.value)) else None


def isolate(token):
    """Convert parsed token into a trait product."""
    token.group["number"] = [v.strip() for v in token.group["value"].split("x")]
    return convert(token)


def convert_many(token):
    """Convert several values."""
    values = token.group["value"]
    units = as_list(token.group.get("len_units", []))

    traits = []
    for i, value in enumerate(values):
        trait = Trait(start=token.start, end=token.end)
        if i < len(units):
            trait.units = units[i]
            trait.units_inferred = False
        else:
            trait.units = units[-1] if units else None
            trait.units_inferred = True
        trait.value = convert_units.convert_units(to_positive_float(value), trait.units)
        if trait.value > TOO_BIG:
            continue
        add_flags(token, trait)
        traits.append(trait)
    return traits


def fix_up(trait, text):
    """Fix problematic parses."""
    # Try to disambiguate doubles quotes from inches
    return fix_up_inches(trait, text)


EMBRYO_LENGTH = Base(
    name=__name__.split(".")[-1],
    fix_up=fix_up,
    rules=[
        VOCAB["uuid"],  # UUIDs cause problems with numbers
        VOCAB["shorthand"],
        VOCAB.part(
            "embryo_len_key",
            r"""
            (?<! collector [\s=:.] ) (?<! reg [\s=:.] ) (
                ( crown | cr ) ( [_\s\-] | \s+ to \s+ )? rump
                | (?<! [a-z] ) crl (?! [a-z] )
                | (?<! [a-z] ) c \.? r \.? (?! [a-z] )
            )""",
        ),
        VOCAB.part("len", r" (length | len) (?! [a-z] ) "),
        VOCAB.part("other", r" \( \s* \d+ \s* \w+ \s* \) "),
        VOCAB.part("separator", r' [;"/.] '),
        VOCAB.grouper("value", """ cross | number len_units? (?! sex ) """),
        VOCAB.grouper("key", """ embryo_len_key len? ( eq | colon )? """),
        VOCAB.grouper(
            "count",
            """
            number side number side eq?
            | number plus number ( eq number )?
            """,
        ),
        VOCAB.grouper("skip", " prep word cross | other | side "),
        VOCAB.producer(convert, """ embryo? key value quest? """),
        VOCAB.producer(convert, """ embryo? x? value key quest? """),
        VOCAB.producer(convert_many, """ embryo count? value{2,} (?! skip ) quest? """),
        VOCAB.producer(convert, """ embryo? key x? value quest? """),
        VOCAB.producer(convert, """ embryo? x? value key quest? """),
        VOCAB.producer(convert, """ embryo x? value (?! skip ) quest? """),
        VOCAB.producer(isolate, """ embryo colon? count? value len_units quest? """),
    ],
)
