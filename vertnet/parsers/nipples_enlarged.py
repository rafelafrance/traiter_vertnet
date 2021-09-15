"""Parse nipple state notations."""

from traiter.old.vocabulary import Vocabulary

import vertnet.pylib.shared_reproductive_patterns as patterns
from vertnet.parsers.base import Base
from vertnet.pylib.trait import Trait

VOCAB = Vocabulary(patterns.VOCAB)


def convert(token):
    """Convert parsed token into a trait."""
    trait = Trait(
        value='enlarged' if token.group.get('enlarged') else 'not enlarged',
        start=token.start,
        end=token.end,
    )
    return trait


NIPPLES_ENLARGED = Base(
    name=__name__.split('.')[-1],
    rules=[
        VOCAB['conj'],
        VOCAB.part('separator', r' [;"?/,] '),

        VOCAB.term('false', """ false """),

        VOCAB.producer(convert, r""" (?P<enlarged> nipple enlarged ) """),
        VOCAB.producer(convert, r""" (?P<enlarged> enlarged nipple ) """),

        VOCAB.producer(convert, r""" (?P<not_enlarged> none nipple ) """),
        VOCAB.producer(convert, r""" (?P<not_enlarged> nipple none ) """),
        VOCAB.producer(convert, r""" (?P<not_enlarged> nipple not_enlarged ) """),
        VOCAB.producer(convert, r"""(?P<not_enlarged> not_enlarged false? nipple )"""),
    ])
