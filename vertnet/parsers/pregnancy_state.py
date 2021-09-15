"""Parse pregnancy state notations."""

from traiter.old.vocabulary import Vocabulary

import vertnet.pylib.shared_reproductive_patterns as patterns
from vertnet.parsers.base import Base
from vertnet.pylib.trait import Trait

VOCAB = Vocabulary(patterns.VOCAB)


def convert(token):
    """Convert parsed token into a trait."""
    trait = Trait(
        value="pregnant" if token.group.get("pos") else "not pregnant",
        start=token.start,
        end=token.end,
    )
    return trait


PREGNANCY_STATE = Base(
    name=__name__.split(".")[-1],
    rules=[
        VOCAB.term(
            "pregnant",
            r""" prega?n?ant pregnan preg pregnancy pregnancies gravid """.split(),
        ),
        VOCAB.part("separator", r' [;,"] '),

        VOCAB.producer(convert, """ (?P<neg> pregnant none) """),
        VOCAB.producer(convert, """ (?P<neg> none pregnant ) """, ),

        VOCAB.producer(convert, """ (?P<pos> pregnant ) """),
    ],
)
