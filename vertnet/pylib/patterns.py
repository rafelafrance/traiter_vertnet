"""Shared token patterns."""

from traiter.old.vocabulary import Vocabulary, FIRST, LOWEST
from vertnet.pylib.util import ORDINALS, NUM_WORDS


VOCAB = Vocabulary()


# Chars that may be a token
VOCAB.part('slash', r' [/] ', capture=False)
VOCAB.part('dash', r' \p{Pd} ', capture=False)
VOCAB.part('open', r' \p{Ps} ', capture=False)
VOCAB.part('close', r' \p{Pe} ', capture=False)
VOCAB.part('x', r' [x×] ', capture=False)
VOCAB.part('quest', r' [?] ')
VOCAB.part('comma', r' [,] ', capture=False, priority=LOWEST)
VOCAB.part('semicolon', r' [;] ', capture=False, priority=LOWEST)
VOCAB.part('colon', r' [:] ', capture=False, priority=LOWEST)
VOCAB.part('ampersand', r' [&] ', capture=False)
VOCAB.part('eq', r' [=] ', capture=False)
VOCAB.part('plus', r' [+] ', capture=False)
VOCAB.part('under', r' [_] ', capture=False)
VOCAB.part('eol', r' [\n\r\f] ', capture=False)
VOCAB.part('dot', r' [.] ', capture=False)

# Small words
VOCAB.part('by', r' by ', capture=False)
VOCAB.part('to', r' to ', capture=False)
VOCAB.part('with', r' with ', capture=False)
VOCAB.part('up_to', r' ( up \s+ )? to ', capture=False)
VOCAB.term('and', r' and ', capture=False)
VOCAB.term('conj', ' or and '.split(), capture=False)
VOCAB.term('prep', ' to with on of in '.split(), capture=False)
VOCAB.term('found', 'found', capture=False)

# NOTE: Double quotes as inches is handled elsewhere
VOCAB.part('inches', r"""
    (?<! [a-z] ) ( inch e? s? | in s? (?! [a-ru-wyz] ) ) """)
VOCAB.part('feet', r"""
    (?<! [a-z] ) ( foot s? | feet s? | ft s? (?! [,\w]) ) | (?<= \d ) ' """)
VOCAB.part('metric_len', r"""
    ( milli | centi )? meters? | ( [cm] [\s.]? m ) (?! [a-ru-wyz] ) """)
VOCAB.grouper('len_units', ' metric_len feet inches'.split())

VOCAB.part('pounds', r' pounds? | lbs? ')
VOCAB.part('ounces', r' ounces? | ozs? ')
METRIC_MASS = r"""
    milligrams? | kilograms? | grams?
    | (?<! [a-z] )( m \.? g s? | k \.? \s? g a? | g[mr]? s? )(?! [a-z] )
    """
VOCAB.part('metric_mass', METRIC_MASS)
VOCAB.grouper('mass_units', 'metric_mass pounds ounces'.split())

VOCAB.grouper('us_units', 'feet inches pounds ounces'.split())
VOCAB.grouper('units', 'len_units mass_units'.split())

# # UUIDs cause problems when extracting certain shorthand notations.
VOCAB.part('uuid', r"""
    \b [0-9a-f]{8} - [0-9a-f]{4} - [1-5][0-9a-f]{3}
        - [89ab][0-9a-f]{3} - [0-9a-f]{12} \b """,
           capture=False, priority=FIRST)

# Time units
VOCAB.part('time_units', r'years? | months? | weeks? | days? | hours?')

# Integers, no commas or signs and typically small
VOCAB.part('integer', r""" \d+ (?! [%\d\-] ) """)

# Date
VOCAB.part('month_name', """
    (?<! [a-z])
    (?P<month>
        january | february | march | april | may | june | july | august
        | september | october | november | december
        | jan | feb | mar | apr | jun | jul | aug | sept? | oct | nov | dec
    )
    (?! [a-z] )
    """, capture=False)

VOCAB.term('word', r' ( [a-z] \w* ) ', capture=False, priority=LOWEST)

# This is a common notation: "11-22-33-44:99g".
# There are other separators "/", ":", etc.
# There is also an extended form that looks like:
#   "11-22-33-44-fa55-hb66:99g" There may be several extended numbers.
#
#   11 = total length (ToL or TL) or sometimes head body length
#   22 = tail length (TaL)
#   33 = hind foot length (HFL)
#   44 = ear length (EL)
#   99 = body mass is optional, as is the mass units
#
# Unknown values are filled with "?" or "x".
#   E.g.: "11-x-x-44" or "11-?-33-44"
#
# Ambiguous measurements are enclosed in brackets.
#   E.g.: 11-[22]-33-[44]:99g

VOCAB.part('shorthand_key', r"""
    (on \s* tag | specimens? (?! \s* [a-z] )
        | catalog (?! [a-z] )) (?! \s* [#] )
    | ( measurement s? | meas ) [:.,]{0,2} ( \s* length \s* )?
        (
            \s* [({\[})]?
                (t [o.]? l [._]? (?! [a-z.] )
                | [a-z]{1,2}) [)}\]]? \.?
        )?
    | tag \s+ \d+ \s* =? ( male | female)? \s* ,
    | measurements? | mesurements? | measurementsnt
    """)

# A possibly unknown value
SH_NUM = r""" \d+ ( \. \d+ )? | (?<= [^\d] ) \. \d+ """
VOCAB.part('sh_num', SH_NUM)

SH_VAL = f' ( {SH_NUM} | [?x]{{1,2}} | n/?d ) '
VOCAB.part('sh_val', SH_VAL)

VOCAB.part('shorthand', fr"""
    (?<! [\d/a-z-] )
    (?P<shorthand_tl> (?P<estimated_tl> \[ )? {SH_VAL} \]? )
    (?P<shorthand_sep> [:/-] )
    (?P<shorthand_tal> (?P<estimated_tal> \[ )? {SH_VAL} \]? )
    (?P=shorthand_sep)
    (?P<shorthand_hfl> (?P<estimated_hfl> \[ )? {SH_VAL} \]? )
    (?P=shorthand_sep)
    (?P<shorthand_el> (?P<estimated_el> \[ )? {SH_VAL} \]? )
    (?P<shorthand_ext> ( (?P=shorthand_sep) [a-z]{{1,4}} {SH_VAL} )* )
    ( [\s=:/-] \s?
        (?P<estimated_wt> \[? \s* )
        (?P<shorthand_wt> {SH_VAL} ) \s*
        \]?
        (?P<shorthand_wt_units> {METRIC_MASS} )?
        \s? \]?
    )?
    (?! [\d/:=a-z-] )
    """)

VOCAB.part('shorthand_bats', fr"""
    (?<! [\d/a-z-] )
    (?P<shorthand_tl> (?P<estimated_tl> \[ )? {SH_VAL} \]? )
    (?P<shorthand_sep> [:/-] )
    (?P<shorthand_tal> (?P<estimated_tal> \[ )? {SH_VAL} \]? )
    (?P=shorthand_sep)
    (?P<shorthand_hfl> (?P<estimated_hfl> \[ )? {SH_VAL} \]? )
    (?P=shorthand_sep)
    (?P<shorthand_el> (?P<estimated_el> \[ )? {SH_VAL} \]? )
    (?P=shorthand_sep)
    (
        (?P<shorthand_tr> (?P<estimated_tr> \[ )? {SH_VAL} \]? \(?tr\)? )
        (
          (?P=shorthand_sep)
          (?P<shorthand_fa> (?P<estimated_fa> \[ )? {SH_VAL} \]? (\(?fa\)?)? )
        )?
        |
        (?P<shorthand_fa> (?P<estimated_fa> \[ )? {SH_VAL} \]? \(?fa\)? )
        (
          (?P=shorthand_sep)
          (?P<shorthand_tr> (?P<estimated_tr> \[ )? {SH_VAL} \]? (\(?tr\)?)? )
        )?
        |
        (?P<shorthand_tr> (?P<estimated_tr> \[ )? {SH_VAL} \]? )
        (?P=shorthand_sep)
        (?P<shorthand_fa> (?P<estimated_fa> \[ )? {SH_VAL} \]? \(?fa\)? )
        |
        (?P<shorthand_fa> (?P<estimated_fa> \[ )? {SH_VAL} \]? )
        (?P=shorthand_sep)
        (?P<shorthand_tr> (?P<estimated_tr> \[ )? {SH_VAL} \]? \(?tr\)? )
        |
        (?P<shorthand_fa> (?P<estimated_fa> \[ )? {SH_VAL} \]? )
        (
          (?P=shorthand_sep)
          (?P<shorthand_tr> (?P<estimated_tr> \[ )? {SH_VAL} \]? )
        )?
    )
    ( [\s=:/-] \s?
        (?P<estimated_wt> \[? \s? )
        (?P<shorthand_wt> {SH_VAL} ) \s?
        \]?
        (?P<shorthand_wt_units> {METRIC_MASS} )?
        \s? \]?
    )?
    (?! [\d/:=a-z-] )
    """)

# Sometimes the last number is missing. Be careful to not pick up dates.
VOCAB.part('shorthand_triple', fr"""
    (?<! [\d/a-z-] )
    (?P<shorthand_tl> (?P<estimated_tl> \[ )? {SH_VAL} \]? )
    (?P<shorthand_sep> [:/-] )
    (?P<shorthand_tal> (?P<estimated_tal> \[ )? {SH_VAL} \]? )
    (?P=shorthand_sep)
    (?P<shorthand_hfl> (?P<estimated_hfl> \[ )? {SH_VAL} \]? )
    (?! [\d/:=a-z-] )
    """)

# Some numeric values are reported as ordinals or words
VOCAB.part('ordinals', ORDINALS)
VOCAB.term('num_words', NUM_WORDS)

# Time units
VOCAB.part('time_units', ' years? months? weeks? days? hours? '.split())

# Side keywords
VOCAB.part('side', r"""
    (?<! [a-z] ) [lr] (?! [a-z] )
    | both | left | right | lft? | lt | rt """)

DIMENSION = r' (?P<dim> length | width ) '
VOCAB.part('dimension', DIMENSION)

# Numeric sides interfere with number parsing so combine \w dimension
VOCAB.part(
    'dim_side',
    fr""" {DIMENSION} \s* (?P<side> [12] ) \b """)

VOCAB.part('cyst', r"""
    (\d+ \s+)? (cyst s? | bodies | cancerous | cancer ) ( \s+ ( on | in ))?""")

# Numbers are positive decimals and estimated values are enclosed in brackets
VOCAB.part('number', r"""
    (?P<estimated_value> \[ )?
    ( ( \d{1,3} ( , \d{3} ){1,3} | \d+ ) ( \. \d+ )?
        | (?<= [^\d] ) \. \d+ | ^ \. \d+ )
    \]?
    """)

# A number or a range of numbers like "12 to 34" or "12.3-45.6"
# Note we want to exclude dates and to not pick up partial dates
# So: no part of "2014-12-11" would be in a range
VOCAB.grouper('mass_range', """
    (?<! dash )
    ( number mass_units? (( dash | to ) number mass_units?)? )
    (?! dash | len_units ) """, capture=False)

# A number or a range of numbers like "12 to 34" or "12.3-45.6"
# Note we want to exclude dates and to not pick up partial dates
# So: no part of "2014-12-11" would be in a range
VOCAB.grouper('len_range', """
    (?<! dash )
    ( number (?P<units> len_units )?
    (( dash | to ) number (?P<units> len_units )? )? )
    (?! dash | mass_units ) """, capture=False)

# A rule for parsing a compound weight like 2 lbs. 3.1 - 4.5 oz
VOCAB.grouper('compound_len', """
    (?P<ft> number ) feet comma?
    (?P<in> number ) ( ( dash | to ) (?P<in> number ) )? inches
    """, capture=False)

# A rule for parsing a compound weight like 2 lbs. 3.1 - 4.5 oz
VOCAB.grouper('compound_wt', """
    (?P<lbs> number ) pounds comma?
    (?P<ozs> number ) ( ( dash | to ) (?P<ozs> number ) )? ounces
    """, capture=False)

# A number times another number like: "12 x 34" this is typically
# length x width. We Allow a triple like "12 x 34 x 56" but we only take
# the first two numbers
CROSS = """ (?<! x )
        ( number len_units? ( x | by ) number len_units?
        | number len_units ) """
VOCAB.grouper('cross', CROSS, capture=False)

# Handle 2 cross measurements, one per left/right side
VOCAB.grouper('joiner', ' ampersand comma and '.split())

VOCAB.grouper('side_cross', """
    (?P<side_1> side )?
        (?P<value_1> number ) (?P<units_1> len_units )?
            ( x | by ) (?P<value_1> number ) (?P<units_1> len_units )?
    joiner?
    (?P<side_2> side )?
        (?P<value_2> number ) (?P<units_2> len_units )?
            ( x | by ) (?P<value_2> number ) (?P<units_2> len_units )?
    (?! mass_units )
    """, capture=False)

# For fractions like "1 2/3" or "1/2".
# We don't allow dates like "1/2/34".
VOCAB.grouper('len_fraction', """
    (?P<whole> number )?
    (?<! slash )
    (?P<numerator> number) slash (?P<denominator> number)
    (?! slash ) (?P<units> len_units)? (?! mass_units ) """, capture=False)
