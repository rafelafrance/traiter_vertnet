"""Parse lactation state notations."""
from traiter.pylib.old.vocabulary import Vocabulary

import vertnet.pylib.shared_reproductive_patterns as patterns
from vertnet.parsers.base import Base
from vertnet.pylib.trait import Trait
from vertnet.pylib.util import to_positive_int

VOCAB = Vocabulary(patterns.VOCAB)

TOO_MANY = 100


def convert(token):
    """Convert single value tokens into a result."""
    value = token.group.get("value")

    if not value:
        return None

    trait = Trait(start=token.start, end=token.end)
    trait.value = to_positive_int(value)

    if trait.value > TOO_MANY:
        return None

    if token.group.get("notation"):
        trait.notation = token.group["notation"]

    return trait


def typed(token):
    """Convert single value tokens into a result."""
    trait = Trait(start=token.start, end=token.end)
    trait.notation = token.group["notation"]
    trait.value = to_positive_int(token.group["value1"])
    trait.value += to_positive_int(token.group.get("value2"))
    return trait


NIPPLE_COUNT = Base(
    name=__name__.split(".")[-1],
    rules=[
        VOCAB["uuid"],  # UUIDs cause problems with numbers
        VOCAB.term("id", r" \d+-\d+ "),
        VOCAB.term("adj", r""" inguinal ing pectoral pec pr """.split()),
        VOCAB.part("number", r" number | no | [#] "),
        VOCAB.part("eq", r" is | eq | equals? | [=] "),
        # Skip arbitrary words
        VOCAB["word"],
        VOCAB["sep"],
        VOCAB.grouper("count", " (?: integer | none )(?! side ) "),
        VOCAB.grouper("modifier", "adj visible".split()),
        VOCAB.grouper("skip", " number eq? integer "),
        VOCAB.producer(
            typed,
            """ (?P<notation>
                    (?P<value1> count) modifier
                    (?P<value2> count) modifier
                ) nipple
            """,
        ),
        # Eg: 1:2 = 6 mammae
        VOCAB.producer(
            convert,
            """ nipple op?
                (?P<notation> count modifier?
                    op? count modifier?
                    (eq (?P<value> count))? )
            """,
        ),
        # Eg: 1:2 = 6 mammae
        VOCAB.producer(
            convert,
            """ (?P<notation> count modifier? op? count modifier?
                (eq (?P<value> count))? ) nipple """,
        ),
        # Eg: 6 mammae
        VOCAB.producer(convert, """ (?P<value> count ) modifier? nipple """),
        # Eg: nipples 5
        VOCAB.producer(convert, """ nipple (?P<value> count ) """),
    ],
)
