"""Parse placental scar counts."""

from traiter.old.vocabulary import Vocabulary

import vertnet.pylib.shared_reproductive_patterns as patterns
from vertnet.parsers.base import Base
from vertnet.pylib.trait import Trait
from vertnet.pylib.util import to_positive_int

VOCAB = Vocabulary(patterns.VOCAB)


def convert_count(token):
    """Convert parsed tokens into a result."""
    trait = Trait(start=token.start, end=token.end)

    value = to_positive_int(token.group.get('value'))
    count1 = to_positive_int(token.group.get('count1'))
    count2 = to_positive_int(token.group.get('count2'))

    if not value:
        value = count1 + count2

    if value >= 1000:
        return None

    trait.value = 'present' if value > 0 else 'absent'

    return trait


def convert_state(token):
    """Convert parsed tokens into a result."""
    trait = Trait(value='present', start=token.start, end=token.end)
    return trait


PLACENTAL_SCAR_STATE = Base(
    name=__name__.split('.')[-1],
    rules=[
        VOCAB['uuid'],  # UUIDs cause problems with numbers

        VOCAB['shorthand'],

        # Adjectives to placental scars
        VOCAB.term('adj', r""" faint prominent recent old possible """.split()),

        # Skip arbitrary words
        VOCAB['word'],
        VOCAB.part('sep', r' [;/] '),

        VOCAB.grouper('count', """
            none embryo conj | none visible | integer | none """),

        VOCAB.producer(convert_count, [
            """(?P<count1> count ) op (?P<count2> count )
                ( eq (?P<value> count ) )? plac_scar """]),

        VOCAB.producer(convert_count, [
            """ plac_scar op?
                  (?P<count1> count ) prep? side
                ( (?P<count2> count ) prep? side )? """]),

        VOCAB.producer(convert_count, [
            """ (?P<count1> count ) prep? side plac_scar
                ( (?P<count2> count ) prep? side (plac_scar)? )? """]),

        VOCAB.producer(convert_count, [
            """ side (?P<count1> count )
                    (visible | op)? plac_scar
                ( side (?P<count2> count )
                    (visible)? (visible | op)? plac_scar? )? """]),

        VOCAB.producer(convert_count, [
            """ (?<! lut )
                (?P<count1> count ) prep? side
                ( (?P<count2> count ) prep? side )?
                plac_scar """]),

        VOCAB.producer(convert_count, [
            """ (?P<count1> count ) plac_scar side
                ( (?P<count2> count ) plac_scar? side )? """]),

        VOCAB.producer(convert_count, [
            """ plac_scar side (?P<count1> count )
                ( plac_scar side (?P<count2> count ) )? """]),

        VOCAB.producer(convert_count, [
            """plac_scar
                (?P<count1> count ) op
                (?P<count2> count )
                ( eq (?P<value> count ) )? """]),

        VOCAB.producer(convert_count, [
            """ (?P<value> count ) adj? plac_scar op?
                ( (?P<count1> count ) side op? (?P<count2> count ) side )?
                """]),

        VOCAB.producer(convert_count, [
            """ (?P<value> count ) embryo? plac_scar (?! count ) """]),

        VOCAB.producer(convert_count, [
            """ plac_scar eq? (?P<value> count ) side """]),

        VOCAB.producer(convert_count, [""" plac_scar eq? (?P<value> count ) """]),

        VOCAB.producer(convert_state, """ plac_scar """),

    ])
