"""Parse hind foot length notations."""
from functools import partial

from traiter.pylib.old.vocabulary import Vocabulary

from vertnet.parsers.base import Base
from vertnet.pylib import patterns
from vertnet.pylib.numeric import fix_up_inches, fraction, shorthand_length, simple

VOCAB = Vocabulary(patterns.VOCAB)


def fix_up(trait, text):
    """Fix problematic parses."""
    # Try to disambiguate doubles quotes from inches
    return fix_up_inches(trait, text)


HIND_FOOT_LENGTH = Base(
    name=__name__.split(".")[-1],
    rules=[
        VOCAB["uuid"],  # UUIDs cause problems with numbers
        # Units are in the key, like: HindFootLengthInMillimeters
        VOCAB.term(
            "key_with_units",
            r"""( hind \s* )? foot \s* ( length | len ) \s* in \s*
                    (?P<units> millimeters | mm )
            """,
        ),
        # Standard keywords that indicate a hind foot length follows
        VOCAB.term(
            "key",
            [
                r"hind \s* foot \s* with \s* (?P<includes> claw )",
                r"hind \s* foot ( \s* ( length | len ) )?",
                "hfl | hf",
            ],
        ),
        # Some patterns require a separator
        VOCAB.part("sep", r" [;,] | $ ", capture=False),
        VOCAB.grouper("noise", " word dash ".split()),
        # Handle fractional values like: hindFoot 9/16"
        VOCAB.producer(
            fraction,
            [
                "key len_fraction units",  # E.g.: hindFoot = 9/16 inches
                "key len_fraction",  # E.g.: hindFoot = 9/16
            ],
        ),
        # A typical hind-foot notation
        VOCAB.producer(
            simple,
            [
                "key_with_units len_range",  # E.g.: hindFootLengthInMM=9-10
                "key noise? len_range units ",  # E.g.: hindFootLength=9-10 mm
                "key noise? len_range",  # Missing units like: hindFootLength 9-10
                "key dash number units",
            ],
        ),
        VOCAB.producer(
            partial(shorthand_length, measurement="shorthand_hfl"),
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
