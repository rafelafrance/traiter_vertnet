"""Parse embryo counts."""

from traiter.old.vocabulary import Vocabulary
from traiter.util import as_list

import vertnet.pylib.shared_reproductive_patterns as patterns
from vertnet.parsers.base import Base
from vertnet.pylib.trait import Trait
from vertnet.pylib.util import to_positive_int

VOCAB = Vocabulary(patterns.VOCAB)

SUB = {"l": "left", "r": "right", "m": "male", "f": "female"}


def convert(token):
    """Convert parsed tokens into a result."""
    trait = Trait(start=token.start, end=token.end)

    if token.group.get("total"):
        trait.value = to_positive_int(token.group["total"])

    elif token.group.get("subcount"):
        trait.value = sum(to_positive_int(c) for c in as_list(token.group["subcount"]))

    if token.group.get("subcount") and token.group.get("sub"):
        for count, sub in zip(
            as_list(token.group["subcount"]), as_list(token.group.get("sub"))
        ):
            count = '1' if count == '!' else count
            sub = SUB.get(sub[0].lower(), sub)
            setattr(trait, sub, to_positive_int(count))

    elif token.group.get("side"):
        side = token.group["side"].lower()
        trait.side = SUB.get(side, side)

    return trait if all(x < 1000 for x in as_list(trait.value)) else None


def found(token):
    """Count the found embryo."""
    token.group["total"] = "1"
    return convert(token)


EMBRYO_COUNT = Base(
    name=__name__.split(".")[-1],
    rules=[
        VOCAB["uuid"],  # UUIDs cause problems with numbers
        VOCAB["shorthand"],
        VOCAB["metric_mass"],
        VOCAB.part(
            "sex",
            r""" males? | females? | (?<! [a-z] ) [mf] (?! [a-z] ) """,
        ),
        VOCAB.term('repo_key', r""" reproductive \s data """),
        VOCAB.term("near_term", r" near[\s-]?term"),
        VOCAB.term("skip", r" w  wt ".split()),
        VOCAB.part("sep", r" [;] "),
        VOCAB.part("bang", r" [!] "),
        VOCAB.grouper(
            "count",
            """ none (word | plac_scar) conj | integer | none | num_words | bang """,
        ),
        VOCAB.grouper("present", " found | near_term "),
        VOCAB.producer(
            convert,
            """ (?P<total> count ) embryo (?! plac_scar ) """,
        ),
        VOCAB.producer(
            convert,
            """ (?P<total> count ) embryo
                (?P<subcount> count ) (?P<sub> side | sex ) conj?
                (?P<subcount> count ) (?P<sub> side | sex )
            """,
        ),
        VOCAB.producer(
            convert,
            """ (?P<total> count ) embryo ( x? integer metric_len )?
                (?P<subcount> count ) (?P<sub> side ) conj?
                (?P<subcount> count ) (?P<sub> side )
            """,
        ),
        VOCAB.producer(
            convert,
            """ (?P<total> count ) ( near_term )? embryo
                (?P<subcount> count ) (?P<sub> side ) conj?
                (?P<subcount> count ) (?P<sub> side )
            """,
        ),
        VOCAB.producer(
            convert,
            """ embryo (?P<total> count ) x integer metric_len?
                (?P<sub> side ) (?P<subcount> count ) conj?
                (?P<sub> side ) (?P<subcount> count )
            """,
        ),
        VOCAB.producer(
            convert,
            """ embryo (?P<subcount> count ) (?P<sub> side ) ( conj | x )?
                       (?P<subcount> count ) (?P<sub> side )
            """,
        ),
        VOCAB.producer(
            convert,
            """ embryo (?P<subcount> count ) (?P<sub> side )
                            ( word | integer | metric_len ){,3}
                       (?P<subcount> count ) (?P<sub> side )
            """,
        ),
        VOCAB.producer(
            convert,
            """ (?P<subcount> count ) (?P<sub> side ) conj?
                (?P<subcount> count ) (?P<sub> side ) embryo
            """,
        ),
        VOCAB.producer(
            convert,
            """ (?P<total> count ) ( size | word )? embryo (?! plac_scar ) """,
        ),
        VOCAB.producer(
            convert,
            """ (?P<total> count ) ( size | word )? embryo (?! plac_scar )
                (?P<subcount> count ) (?P<sub> side ) conj?
                (?P<subcount> count ) (?P<sub> side )
            """,
        ),
        VOCAB.producer(
            convert,
            """ (?P<subcount> count ) embryo word? (?P<sub> side ) ( conj | word )?
                (?P<subcount> count ) word? (?P<sub> side )
            """,
        ),
         VOCAB.producer(
            convert,
            """ repo_key word? (?P<subcount> count ) (?P<sub> side ) word?
                               (?P<subcount> count ) (?P<sub> side )
            """,
        ),
         VOCAB.producer(
            convert,
            """ repo_key? word? (?P<total> count ) ( x? integer metric_len )? embryo
                    (?P<subcount> count ) (?P<sub> side ) word?
                    (?P<subcount> count ) (?P<sub> side )
            """,
        ),
       VOCAB.producer(
            convert,
            """ (?P<sub> side ) (?P<subcount> count ) embryo
                ( x integer )?
                (?P<sub> side ) (?P<subcount> count ) embryo?
            """,
        ),
       VOCAB.producer(
            convert,
            """ embryo (?P<sub> side ) (?P<subcount> count )
                            ( word | integer | metric_len ){,3}
                       (?P<sub> side ) (?P<subcount> count ) embryo?
            """,
        ),
       VOCAB.producer(
            convert,
            """ (?P<subcount> count ) (?P<sub> side ) x
                (?P<subcount> count ) (?P<sub> side ) x
                integer metric_len embryo
            """,
        ),
       VOCAB.producer(
            convert,
            """ (?P<sub> side )
                    ( word | integer | metric_len ){,3} (?P<subcount> count )
                    embryo? ( x integer metric_len )
                (?P<sub> side )
                    ( word | integer | metric_len ){,3} (?P<subcount> count )
            """,
        ),
        VOCAB.producer(convert, """ (?P<total> count ) integer metric_len embryo """),
        VOCAB.producer(
            convert,
            """ (?P<total> count ) near_term? embryo  (?! plac_scar ) """,
        ),
        VOCAB.producer(found, """ embryo present | present embryo """),
        VOCAB.producer(found, """ embryo word? (?P<sub> side ) """),
        VOCAB.producer(convert, """ (?P<subcount> count ) embryo (?P<sub> side )"""),
        VOCAB.producer(convert, """ embryo (?P<total> count )"""),
        VOCAB.producer(
            convert,
            """ embryo (?P<subcount> count ) x integer metric_len? (?P<sub> side ) """,
        ),
    ],
)
