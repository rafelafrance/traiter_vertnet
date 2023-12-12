"""Parse testes state notations."""
from traiter.pylib.old.vocabulary import Vocabulary

import vertnet.pylib.shared_reproductive_patterns as patterns
from vertnet.parsers.base import Base
from vertnet.pylib.trait import Trait

VOCAB = Vocabulary(patterns.VOCAB)


def convert(token):
    """Convert parsed token into a trait producer."""
    trait = Trait(
        value="scrotal" if token.group.get("pos") else "not scrotal",
        start=token.start,
        end=token.end,
    )
    return trait


SCROTAL_STATE = Base(
    name=__name__.split(".")[-1],
    rules=[
        VOCAB.term("testes_abbrev", "tes ts tnd td tns ta t".split()),
        VOCAB.term("scrotal_abbrev_pos", "sc".split()),
        VOCAB.term("scrotal_abbrev_neg", "ns ".split()),
        # If possible exclude length. Ex: reproductive data=testes: 11x7 mm
        VOCAB.grouper("length", "cross len_units?"),
        VOCAB.producer(convert, """ (?P<pos> scrotal_pos ) """),
        VOCAB.producer(
            convert,
            """ (?P<pos> (testes | testes_abbrev | label) scrotal_abbrev_pos ) """,
        ),
        VOCAB.producer(
            convert, """ (?P<pos> scrotal_abbrev_pos (testes | testes_abbrev) ) """
        ),
        VOCAB.producer(convert, """ (?P<neg> scrotal_neg ) """),
        VOCAB.producer(convert, """ (?P<neg> scrotal_pos none ) """),
        VOCAB.producer(convert, """ (?P<neg> none scrotal_pos ) """),
        VOCAB.producer(
            convert,
            """ (?P<neg> (testes | testes_abbrev | label) scrotal_abbrev_neg ) """,
        ),
        VOCAB.producer(
            convert, """ (?P<neg> scrotal_abbrev_neg ) (testes | testes_abbrev) """
        ),
    ],
)
