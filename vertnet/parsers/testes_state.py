"""Parse testes state notations."""

from traiter.old.vocabulary import Vocabulary

import vertnet.pylib.shared_reproductive_patterns as patterns
from vertnet.parsers.base import Base
from vertnet.pylib.trait import Trait

VOCAB = Vocabulary(patterns.VOCAB)


def convert(token):
    """Convert parsed token into a trait producer."""
    trait = Trait(value=token.group["value"].lower(), start=token.start, end=token.end)
    trait.is_flag_in_token(token, "ambiguous_key")
    return trait


TESTES_STATE = Base(
    name=__name__.split(".")[-1],
    rules=[
        # Abbreviations for "testes"
        VOCAB.term("abbrev", "tes ts tnd td tns ta t".split()),
        VOCAB["uterus"],
        VOCAB.grouper(
            "state",
            [
                "non fully descended",
                "abdominal non descended",
                "abdominal descended",
                "non descended",
                "fully descended",
                "partially descended",
                "size non descended",
                "size descended",
                "descended",
            ],
        ),
        # Simplify the testes length so it can be skipped easily
        VOCAB.grouper("length", "cross len_units?"),
        VOCAB.producer(
            convert,
            r""" (?P<value>
                ( testes | abbrev | ambiguous_key ) length?
                    ( state | abdominal | size )
                    ( conj? ( state | size ) )?
            ) """,
        ),
        VOCAB.producer(
            convert,
            r""" (?P<value> non ( testes | abbrev | ambiguous_key ) ( state )? ) """,
        ),
        VOCAB.producer(
            convert,
            """ label 
                (?P<value> ( testes | abbrev )? length? size ( conj? state )? )
            """,
        ),
    ],
)
