"""Parse lactation state notations."""

from traiter.old.vocabulary import Vocabulary
import vertnet.pylib.shared_reproductive_patterns as patterns
from vertnet.parsers.base import Base, convert

VOCAB = Vocabulary(patterns.VOCAB)

LACTATION_STATE = Base(
    name=__name__.split('.')[-1],
    rules=[
        VOCAB.part('lactating', r""" (
            lactating | lactation | lactated | lactate | lact
            | lactaing | lactacting | lactataing | lactational
            | oelact | celact | lactati | lactacting | lactatin
            | lactatting | lactatng
            | nursing | suckling
            ) \b """),

        VOCAB.part('not', r' \b ( not | non | no ) '),

        VOCAB.part('post', r""" \b (
            (( just | recently ) \s+ )? finished
            | post | recently | recent | had | pre
            ) """),

        VOCAB.part('pre', r' \b pre [\s\-]? '),

        # Separates measurements
        VOCAB.part('separator', r' [;"/] '),
        VOCAB['word'],

        VOCAB.grouper('prefix', 'not post pre'.split()),

        VOCAB.producer(
            convert, """ (?P<value> prefix? lactating quest? ) """),

        ])
