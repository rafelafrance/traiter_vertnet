"""Parse lactation state notations."""

from traiter.old.vocabulary import Vocabulary

import vertnet.pylib.shared_reproductive_patterns as patterns
from vertnet.parsers.base import Base
from vertnet.pylib.trait import Trait

VOCAB = Vocabulary(patterns.VOCAB)


def convert(token):
    """Convert parsed token into a trait."""
    trait = Trait(
        value="lactating" if token.group.get("pos") else "not lactating",
        start=token.start,
        end=token.end,
    )
    return trait


LACTATION_STATE = Base(
    name=__name__.split(".")[-1],
    rules=[
        VOCAB.part(
            "lactating",
            r""" (
                lactating | lactation | lactated | lactate | lact
                | lactaing | lactacting | lactataing | lactational
                | oelact | celact | lactati | lactacting | lactatin
                | lactatting | lactatng
                | nursing | suckling
                ) \b
            """,
        ),
        VOCAB.term("lactating_abbrev", r"[oc][esm]l"),
        VOCAB.term("not_lactating_abbrev", r"[oc][esm]n"),
        VOCAB.term("post", r""" post | finished """),

        # Separates measurements
        VOCAB.part("separator", r' [;"/] '),

        VOCAB.producer(convert, """ (?P<pos> lactating ) """),
        VOCAB.producer(convert, """ (?P<pos> lactating_abbrev ) """),

        VOCAB.producer(convert, """ (?P<neg> (none | post) lactating ) """),
        VOCAB.producer(convert, """ (?P<neg> lactating (none | post) ) """),
        VOCAB.producer(convert, """ (?P<neg> not_lactating_abbrev ) """),
    ],
)
