"""Parse forearm length notations."""

from functools import partial
from traiter.vocabulary import Vocabulary
from vertnet.pylib.numeric import fix_up_inches, shorthand_length
from vertnet.pylib.numeric import fraction, simple
import vertnet.pylib.patterns as patterns
from vertnet.parsers.base import Base

VOCAB = Vocabulary(patterns.VOCAB)


def fix_up(trait, text):
    """Fix problematic parses."""
    # Try to disambiguate doubles quotes from inches
    return fix_up_inches(trait, text)


FOREARM_LENGTH = Base(
    name=__name__.split('.')[-1],
    rules=[
        VOCAB['uuid'],  # UUIDs cause problems with numbers

        # Units are in the key, like: ForearmLengthInMillimeters
        VOCAB.term(
            'key_with_units',
            r"""( forearm \s* )? \s* ( length | len ) \s* in \s*
                    (?P<units> millimeters | mm )"""),

        # Standard keywords that indicate a forearm length follows
        VOCAB.term('key', r"""
            forearm  ( \s* ( length | len ) )?
            | fore? \s? [.]? \s? a
            | fa
            """),

        # Some patterns require a separator
        VOCAB.part('sep', r' [;,] | $ ', capture=False),

        VOCAB.grouper('noise', ' word dash '.split()),

        # Handle fractional values like: forearm 9/16"
        VOCAB.producer(fraction, [
            'key len_fraction units',   # E.g.: forearm = 9/16 inches
            'key len_fraction',         # E.g.: forearm = 9/16
            ]),

        # A typical hind-foot notation
        VOCAB.producer(simple, [
            'key_with_units len_range',     # E.g.: forearmLengthInMM=9-10
            'key noise? len_range units ',  # E.g.: forearmLength=9-10 mm
            'key noise? len_range',  # Missing units like: forearm 9-10
            'key dash number units?',
            ]),

        VOCAB.producer(partial(
            shorthand_length,
            measurement='shorthand_fl'), [
            'shorthand_key shorthand',       # With a key
            'shorthand',                     # Without a key
            'shorthand_key shorthand_bats',  # With a key
            'shorthand_bats',                # Without a key
            ]),

        ])
