"""Parse tragus length notations."""

from traiter.old.vocabulary import Vocabulary
from vertnet.pylib.numeric import fix_up_inches
from vertnet.pylib.numeric import fraction, simple
import vertnet.pylib.patterns as patterns
from vertnet.parsers.base import Base

VOCAB = Vocabulary(patterns.VOCAB)


def fix_up(trait, text):
    """Fix problematic parses."""
    # Try to disambiguate doubles quotes from inches
    return fix_up_inches(trait, text)


TRAGUS_LENGTH = Base(
    name=__name__.split('.')[-1],
    rules=[
        VOCAB['uuid'],  # UUIDs cause problems with numbers

        # Units are in the key, like: tragusLengthInMillimeters
        VOCAB.term(
            'key_with_units',
            r"""( tragus \s* ) \s* ( length | len ) \s* in \s*
                    (?P<units> millimeters | mm ) """),

        # Standard keywords that indicate a tragus length follows
        VOCAB.term('key', r"""
            ( tragus | trag | tragi ) \s* (length | len | l )?
            | tr """),

        # Some patterns require a separator
        VOCAB.part('sep', r' [;,] | $ ', capture=False),

        VOCAB.grouper('noise', ' word dash '.split()),

        # Handle fractional values like: tragus 9/16"
        VOCAB.producer(fraction, [
            'key len_fraction units',   # E.g.: tragus = 9/16 inches
            'key len_fraction',         # E.g.: tragus = 9/16
            ]),

        # A typical hind-foot notation
        VOCAB.producer(simple, [
            'key_with_units len_range',     # E.g.: tragusLengthInMM=9-10
            'key noise? len_range units ',  # E.g.: tragusLengthInMM=9-10 mm
            'key noise? len_range',  # Missing units: tragusLengthInMM 9-10
            'key dash? number units?',
            ]),

        ])
