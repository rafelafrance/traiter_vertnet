"""Parse pregnancy state notations."""

from traiter.old.vocabulary import Vocabulary

import vertnet.pylib.shared_reproductive_patterns as patterns
from vertnet.parsers.base import Base, convert

VOCAB = Vocabulary(patterns.VOCAB)

PREGNANCY_STATE = Base(
    name=__name__.split(".")[-1],
    rules=[
        VOCAB.term(
            "pregnant",
            r"""
                prega?n?ant pregnan preg pregnancy pregnancies gravid
                post[\s\-]?parous multiparous nulliparous parous primiparous
            """.split(),
        ),
        VOCAB.term("joiner", r""" of were """.split()),
        VOCAB.term(
            "recent",
            r""" recently recent was previously prev """.split(),
        ),
        VOCAB.term(
            "probably",
            r"""
                probably prob possibly possible
                appears? very
                visible visibly
                evidence evident
            """.split(),
        ),
        VOCAB.term("stage", r" early late mid ".split()),
        VOCAB.part("separator", r' [;,"] '),
        # E.g.: pregnancy visible
        VOCAB.producer(
            convert, """ (?P<value> pregnant joiner? none? probably quest? ) """
        ),
        # E.g.: Probably early pregnancy
        VOCAB.producer(
            convert,
            """ (?P<value> none? (recent | probably)?
                stage? (none | joiner)? pregnant quest? )
            """,
        ),
    ],
)
