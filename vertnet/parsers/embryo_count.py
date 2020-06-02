"""Parse embryo counts."""

from traiter.old.vocabulary import Vocabulary
from vertnet.pylib.util import as_list, to_int
from vertnet.pylib.trait import Trait
import vertnet.pylib.shared_reproductive_patterns as patterns
from vertnet.parsers.base import Base

VOCAB = Vocabulary(patterns.VOCAB)

SUB = {'l': 'left', 'r': 'right', 'm': 'male', 'f': 'female'}


def convert(token):
    """Convert parsed tokens into a result."""
    trait = Trait(start=token.start, end=token.end)

    if token.group.get('total'):
        trait.value = to_int(token.group['total'])

    elif token.group.get('subcount'):
        trait.value = sum(
            to_int(c) for c in as_list(token.group['subcount']))

    if token.group.get('subcount') and token.group.get('sub'):
        for count, sub in zip(as_list(token.group['subcount']),
                              as_list(token.group.get('sub'))):
            sub = SUB.get(sub[0].lower(), sub)
            setattr(trait, sub, to_int(count))

    elif token.group.get('side'):
        side = token.group['side'].lower()
        trait.side = SUB.get(side, side)

    return trait if all(x < 1000 for x in as_list(trait.value)) else None


def found(token):
    """An embryo was found, so count it."""
    token.group['total'] = '1'
    return convert(token)


EMBRYO_COUNT = Base(
    name=__name__.split('.')[-1],
    rules=[
        VOCAB['uuid'],  # UUIDs cause problems with numbers

        VOCAB['shorthand'],

        # The sexes like: 3M or 4Females
        VOCAB.part('sex', r"""
            males? | females? | (?<! [a-z] ) [mf] (?! [a-z] ) """),

        VOCAB.term('near_term', r' near[\s-]?term'),

        VOCAB.term('skip', r' w  wt '.split()),
        VOCAB.part('sep', r' [;] '),

        VOCAB.grouper('count', """
            none (word | plac_scar) conj | integer | none | num_words """),

        VOCAB.grouper('present', ' found | near_term '),

        VOCAB.producer(convert, """
            side (?P<total> count ) embryo (?! plac_scar ) """),

        VOCAB.producer(convert, """
            ( (?P<total> count ) ( word | present )? )?
            embryo ( ( integer (?! side) ) | word )*
            (?P<subcount> count ) (?P<sub> side | sex )
            ( ( conj | prep )? (?P<subcount> count ) (?P<sub> side | sex ) )?
            """),

        VOCAB.producer(convert, """
            (?P<subcount> count ) embryo prep? (?P<sub> side ) word?
            (?P<subcount> count ) embryo? prep? (?P<sub> side )
            """),

        VOCAB.producer(convert, """
            (?P<subcount> count ) (?P<sub> side ) word?
            (?P<subcount> count ) (?P<sub> side ) embryo
            """),

        VOCAB.producer(convert, """
            (?P<total> count ) ( size | word )? embryo (?! plac_scar ) """),

        VOCAB.producer(convert, """
            (?P<total> count ) ( size | word )? embryo (?! plac_scar ) """),

        VOCAB.producer(convert, """ (?P<total> count ) present embryo """),

        VOCAB.producer(found, """ embryo present | present embryo """),

        VOCAB.producer(found, """ embryo prep? present? (?P<sub> side ) """),

        ])
