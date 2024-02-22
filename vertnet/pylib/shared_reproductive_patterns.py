"""Shared reproductive trait tokens (testes & ovaries)."""
from traiter.pylib.old.vocabulary import LOWEST, Vocabulary

from vertnet.pylib import patterns

VOCAB = Vocabulary(patterns.VOCAB)

VOCAB.term("sex", "females? | males? | [f]")

VOCAB.term("active", "active inactive".split())
VOCAB.part("and", r" ( and \b | [&] ) ")
VOCAB.term("count", r"""( only | all | both )? \s* [12]""")

VOCAB.term(
    "color",
    r""" (( dark | light | pale ) \s* )?
         ( red | pink | brown | black | white | pigmented )
    """,
)

VOCAB.term("texture", " smooth ")

VOCAB.term("covered", " covered ")

VOCAB.term("destroyed", "destroy(ed)?")

VOCAB.part(
    "size",
    r"""
        ( very \s+ )?
        ( enlarged | enlarge | large | small | shrunken | shrunk | swollen
            | extended | unobservable | sm-med
            | moderate | mod \b | medium  | med \b | minute | lg \b
            | sm \b | tiny )
        ( \s* size d? | [+] )?
    """,
)

VOCAB.part(
    "not_enlarged",
    r"""
        small | unobservable | sm-med | sm \b | tiny | minute
        | not [\s\-]? enlarged | not [\s\-]? large
    """,
)

VOCAB.part(
    "enlarged",
    r"""
        enlarged | enlarge | large | extended | protuberant | prominent | lg \b
        | conspicuous
    """,
)

VOCAB.part(
    "developed",
    r"""
            ( (fully | incompletely | partially | part | well)
                [.\s-]{0,2} )?"""
    rf"""(developed? | undeveloped? | development | devel
            | dev \b ([\s:]* none | {VOCAB['size'].pattern} )?
            | undevel | undev | indist)
    """,
)

VOCAB.term("fat", " fat ")

VOCAB.part("fully", ["fully", "( in )? complete ( ly )?"])

VOCAB.part("gonads", " (?P<ambiguous_key> gonads? ) ")

VOCAB.part("in", r" in ")

VOCAB.term("label", "reproductive .? ( data | state | condition )")

VOCAB.part("mature", r"( immature | mature | imm ) \b ")

VOCAB.part("non", r" \b ( not | non | no | semi | sub ) ")
VOCAB.term("none", r" no | none | not | non ")

VOCAB.part(
    "partially",
    ["partially", " \\b part \\b", "\\b pt \\b", *"slightly slight barely".split()],
)

VOCAB.part("sep", " [;] | $ ")

VOCAB.part("sign", " [+-] ")

VOCAB.term(
    "visible",
    r""" ( very \s+ )? (
        visible | invisible | hidden | prominent? | seen | conspicuous
            | bare | faint | definite
    ) """,
)

# We allow random words in some situations
VOCAB.part("word", " [a-z]+ ", capture=False, priority=LOWEST)

VOCAB.term("tissue", " tissue ".split())

VOCAB.term("present", " present absent ".split())

# Some traits are presented as an equation
VOCAB.part("op", r" [+:&] ")
VOCAB.part("eq", r" [=] ")

VOCAB.part("abdominal", "abdominal abdomin abdom abd".split())

VOCAB.part("descended", ["( un )? ( des?c?end ( ed )?", "desc? )"])

# Other state words
VOCAB.term("other", "cryptorchism cryptorchid monorchism monorchid inguinal".split())

VOCAB.part("scrotal", r"( nonscrotal | scrotum | scrotal | scrot | nscr | scr) \b")
VOCAB.part("scrotal_pos", r"( scrotum | scrotal | scrot | scr) \b")
VOCAB.part("scrotal_neg", r"( nonscrotal | nscr ) \b")

VOCAB.part("testes", r" ( testes |  testis | testicles? | test ) \b ")

VOCAB.part("alb", r" \b ( albicans | alb ) \b ")

VOCAB.part(
    "corpus",
    r""" \b ( c\.l\. | ( corpus | corpora | corp | cor | c | cl ) \b )""",
)

VOCAB.part("fallopian", r" ( fallopian | foll ) ( \s* tubes? )? ")

VOCAB.term("horns", "horns?")

VOCAB.part("lut", r" ( c \.? l \.\? ) | \b ( luteum | lute | lut ) \b ")

VOCAB.part("ovary", r" ( ovary s? | ovaries | ov ) \b ")

VOCAB.part("uterus", "uterus uterine ut".split())
VOCAB.part("horn", "horns?".split(), capture=False)

VOCAB.part(
    "nipple",
    r""" (
        nipples? | nipp?s? | teats? |
            ((mammae | mamm[ae]ry | mammaries | mamm (?! alian ) )
                (\s+ ( glands? | tisss?ue ) )? )
    ) """,
)

VOCAB.part(
    "embryo",
    r"""
        embryonic | embryos? | embryps? | embroys | embs? | embrs?
        | fetuses | fetus | foeti
        | pregnant
        | embyros?
    """,
)

# Spellings of placental scar
VOCAB.part(
    "plac_scar",
    r"""
        ( placental | plac \b | postnatal | pac \b | \b pl \b )
            [.\s]* ( scarring | scars? )
        | p [\s.-] ( scarring | scars? )
        | ( uterus | uterine | \b ut \b ) [.\s]* ( scarring | scars? )
        | ( scarring | scars? ) \b (?! \s* ( on | above | below ) )
        | ps \b | pslc | plac \b | plscr | plsc
    """,
)

# Gonads can be for female or male
VOCAB.part("ambiguous_key", r" gonads? ")
