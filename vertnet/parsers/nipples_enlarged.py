"""Parse nipple state notations."""
from traiter.pylib.old.vocabulary import Vocabulary

import vertnet.pylib.shared_reproductive_patterns as patterns
from vertnet.parsers.base import Base
from vertnet.pylib.trait import Trait

VOCAB = Vocabulary(patterns.VOCAB)


def convert(token):
    """Convert parsed token into a trait."""
    trait = Trait(
        value="enlarged" if token.group.get("pos") else "not enlarged",
        start=token.start,
        end=token.end,
    )
    return trait


NIPPLES_ENLARGED = Base(
    name=__name__.split(".")[-1],
    rules=[
        VOCAB["conj"],
        VOCAB.part("separator", r' [;"?/,] '),
        VOCAB.term("enlarged_abbrev", r"[oc]e[ln]"),
        VOCAB.term("not_enlarged_abbrev", r"[oc]s[ln]"),
        VOCAB.term("false", """ false """),
        VOCAB.producer(convert, """ (?P<pos> nipple enlarged ) """),
        VOCAB.producer(convert, """ (?P<pos> enlarged nipple ) """),
        VOCAB.producer(convert, """ (?P<pos> enlarged_abbrev ) """),
        VOCAB.producer(convert, """ (?P<neg> none nipple ) """),
        VOCAB.producer(convert, """ (?P<neg> nipple none ) """),
        VOCAB.producer(convert, """ (?P<neg> nipple not_enlarged ) """),
        VOCAB.producer(convert, """ (?P<neg> not_enlarged false? nipple ) """),
        VOCAB.producer(convert, """ (?P<neg> not_enlarged_abbrev ) """),
    ],
)
