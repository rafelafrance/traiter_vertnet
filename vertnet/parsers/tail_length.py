"""Parse tail length notations."""
from functools import partial

import regex
from traiter.pylib.old.vocabulary import Vocabulary

from vertnet.parsers.base import Base
from vertnet.pylib import patterns
from vertnet.pylib.numeric import fix_up_inches, fraction, shorthand_length, simple
from vertnet.pylib.util import RE_FLAGS

VOCAB = Vocabulary(patterns.VOCAB)

# How far to look into the surrounding context to disambiguate the parse
LOOK_BACK_FAR = 40
LOOK_BACK_NEAR = 20

# These indicate that the parse is not really for a tail length
IS_TESTES = regex.compile(
    " reproductive | gonad | test | scrotal | scrotum | scrot ", RE_FLAGS
)
IS_ELEVATION = regex.compile(" elevation | elev ", RE_FLAGS)
IS_TOTAL = regex.compile(" body | nose | snout ", RE_FLAGS)
IS_TAG = regex.compile(" tag ", RE_FLAGS)
IS_ID = regex.compile(" identifier | ident | id ", RE_FLAGS)


def fix_up(trait, text):
    """Fix problematic parses."""
    # Check that this isn't a total length trait
    start = max(0, trait.start - LOOK_BACK_NEAR)
    if IS_TOTAL.search(text, start, trait.start):
        return None

    # Problem parses happen mostly with an ambiguous key
    if trait.ambiguous_key:
        # Make sure this isn't a testes measurement
        start = max(0, trait.start - LOOK_BACK_FAR)
        if (
            IS_TESTES.search(text, start, trait.start)
            or IS_ELEVATION.search(text, start, trait.start)
            or IS_ID.search(text, start, trait.start)
        ):
            return None

        # Make sure this isn't a tag
        start = max(0, trait.start - LOOK_BACK_NEAR)
        if IS_TAG.search(text, start, trait.start):
            return None

    # Try to disambiguate doubles quotes from inches
    return fix_up_inches(trait, text)


TAIL_LENGTH = Base(
    name=__name__.split(".")[-1],
    fix_up=fix_up,
    rules=[
        VOCAB["uuid"],  # UUIDs cause problems with numbers
        # Looking for keys like: tailLengthInMM
        VOCAB.term(
            "key_with_units",
            r"""
                tail \s* ( length | len ) \s* in \s*
                (?P<units> millimeters | mm )
            """,
        ),
        # The abbreviation key, just: t. This can be a problem.
        VOCAB.part(
            "char_key",
            r"""
                \b (?P<ambiguous_key> t ) (?! [a-z] ) (?! _ \D )
            """,
        ),
        # Standard keywords that indicate a tail length follows
        VOCAB.term("keyword", [r" tail \s* length ", r" tail \s* len ", "tail", "tal"]),
        # Some patterns require a separator
        VOCAB.part("sep", r" [;,] | $ ", capture=False),
        # Consider all of these tokens a key
        VOCAB.grouper("key", "keyword char_key".split()),
        # Handle fractional values like: tailLength 9/16"
        VOCAB.producer(
            fraction,
            [
                # E.g.: tail = 9/16 in
                "key len_fraction (?P<units> len_units )",
                "key len_fraction",  # Without units, like: tail = 9/16
            ],
        ),
        VOCAB.producer(
            simple,
            [
                "key_with_units len_range",  # E.g.: tailLengthInMM=9-10
                "key len_range (?P<units> len_units )",  # E.g.: tailLength=9-10 mm
                "key len_range",  # Missing units like: tailLength 9-10
            ],
        ),
        VOCAB.producer(
            partial(shorthand_length, measurement="shorthand_tal"),
            [
                "shorthand",
                "key shorthand_bats",
                "shorthand_bats",
                # Handle a truncated shorthand notation
                "triple_key shorthand_triple (?! shorthand | len_range )",
            ],
        ),
    ],
)
