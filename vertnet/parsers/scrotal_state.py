"""Parse testes state notations."""

from traiter.old.vocabulary import Vocabulary
from vertnet.pylib.trait import Trait
import vertnet.pylib.shared_reproductive_patterns as patterns
from vertnet.parsers.base import Base

VOCAB = Vocabulary(patterns.VOCAB)


def convert(token):
    """Convert parsed token into a trait producer."""
    trait = Trait(
        value=token.group['value'].lower(),
        start=token.start, end=token.end)
    trait.is_flag_in_token(token, 'ambiguous_key')
    return trait


SCROTAL_STATE = Base(
    name=__name__.split('.')[-1],
    rules=[
        VOCAB.term('testes_abbrev', 'tes ts tnd td tns ta t'.split()),

        VOCAB.term('scrotal_abbrev', 'ns sc'.split()),

        # If possible exclude length. Ex: reproductive data=testes: 11x7 mm
        VOCAB.grouper('length', 'cross len_units?'),

        VOCAB.producer(convert, r""" (?P<value>
            ( testes | testes_abbrev ) non? ( scrotal | scrotal_abbrev ) ) """),

        VOCAB.producer(convert, r""" (?P<value> non? scrotal ) """),

        VOCAB.producer(convert, r""" label (?P<value> scrotal_abbrev )  """),

        ])
