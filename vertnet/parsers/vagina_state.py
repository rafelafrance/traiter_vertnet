"""Parse vagina state notations."""

from traiter.old.vocabulary import Vocabulary

import vertnet.pylib.shared_reproductive_patterns as patterns
from vertnet.parsers.base import Base, convert

VOCAB = Vocabulary(patterns.VOCAB)

VAGINA_STATE = Base(
    name=__name__.split(".")[-1],
    rules=[
        VOCAB.part("vagina", r""" (?<! sal ) ( vagina | vag | vulva ) """),
        VOCAB.term("abbrev", r""" ov cv [oc][sme][ln] vc vo """.split()),
        VOCAB.part(
            "closed",
            r"""
                closed | imperforated | imperf | cerrada | non [-\s] perforated
                | unperforate | non  [-\s] perf | clsd | imp
            """,
        ),
        VOCAB.part("open", r""" open | perforated? | perf | abrir """),
        VOCAB.part("other", r""" swollen | plugged | plug | sealed """),

        VOCAB.grouper("state", """ closed | open | other """),

        VOCAB.producer(convert, """ (?P<value> vagina partially? state ) """),
        VOCAB.producer(convert, """ (?P<value> state vagina state? ) """),
        VOCAB.producer(convert, """ (?P<value> ( state | abbrev )  vagina? ) """),
    ],
)
