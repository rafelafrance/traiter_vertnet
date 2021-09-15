"""Test nipples enlarged  notations."""
# pylint: disable=missing-module-docstring,missing-class-docstring
# pylint: disable=missing-function-docstring,too-many-public-methods
import unittest
from vertnet.pylib.trait import Trait
from vertnet.parsers.nipples_enlarged import NIPPLES_ENLARGED


class TestNipplesEnlarged(unittest.TestCase):
    def test_parse_01(self):
        self.assertEqual(
            NIPPLES_ENLARGED.parse("vagina closed, nipples large"),
            [Trait(value="enlarged", start=15, end=28)],
        )

    def test_parse_02(self):
        self.assertEqual(
            NIPPLES_ENLARGED.parse("pregnant; 5 emb; protuberant nipples"),
            [Trait(value="enlarged", start=17, end=36)],
        )

    def test_parse_03(self):
        self.assertEqual(
            NIPPLES_ENLARGED.parse("NO nipple showing"),
            [Trait(value="not enlarged", start=0, end=9)],
        )

    def test_parse_04(self):
        self.assertEqual(
            NIPPLES_ENLARGED.parse("no emb; VERY SMALL FALSE NIPPLES"),
            [Trait(value="not enlarged", start=13, end=32)],
        )

    def test_parse_05(self):
        self.assertEqual(
            NIPPLES_ENLARGED.parse("; NIPPLES INDICATE PREVIOUS LACTATION"), []
        )

    def test_parse_06(self):
        self.assertEqual(
            NIPPLES_ENLARGED.parse("Nipples slightly enlarged."),
            [Trait(value="enlarged", start=0, end=25)],
        )

    def test_parse_07(self):
        self.assertEqual(NIPPLES_ENLARGED.parse("Nipples pigmented."), [])

    def test_parse_08(self):
        self.assertEqual(
            NIPPLES_ENLARGED.parse("no scars or emb., nip. sm., low fat"),
            [Trait(value="not enlarged", start=18, end=25)],
        )

    def test_parse_09(self):
        self.assertEqual(NIPPLES_ENLARGED.parse("; teats visible,"), [])

    def test_parse_10(self):
        self.assertEqual(
            NIPPLES_ENLARGED.parse(", LG UTERUS & TEATS,"),
            [Trait(value="enlarged", start=2, end=19)],
        )

    def test_parse_11(self):
        self.assertEqual(NIPPLES_ENLARGED.parse("4 teats post lac."), [])

    def test_parse_12(self):
        self.assertEqual(
            NIPPLES_ENLARGED.parse("lactating, mammary glands much swollen"), []
        )

    def test_parse_13(self):
        self.assertEqual(
            NIPPLES_ENLARGED.parse("VO, NE, mamm. lg."),
            [Trait(value="enlarged", start=8, end=16)],
        )

    def test_parse_14(self):
        self.assertEqual(NIPPLES_ENLARGED.parse("mammary glands active"), [])

    def test_parse_15(self):
        self.assertEqual(
            NIPPLES_ENLARGED.parse("mammae conspicuous; lactating;"),
            [Trait(value="enlarged", start=0, end=18)],
        )

    def test_parse_16(self):
        self.assertEqual(NIPPLES_ENLARGED.parse("; MAMMARY TISSSUE ABSENT;"), [])

    def test_parse_17(self):
        self.assertEqual(
            NIPPLES_ENLARGED.parse(
                "; reproductive data=no nipples showing, uterus found;"
            ),
            [Trait(value="not enlarged", start=20, end=30)],
        )

    def test_parse_18(self):
        self.assertEqual(
            NIPPLES_ENLARGED.parse("nipples small, moderate fat"),
            [Trait(value="not enlarged", start=0, end=13)],
        )

    def test_parse_19(self):
        self.assertEqual(
            NIPPLES_ENLARGED.parse("uterus enlarged, large nipples"),
            [Trait(value="enlarged", start=17, end=30)],
        )

    def test_parse_20(self):
        self.assertEqual(NIPPLES_ENLARGED.parse("nipples medium"), [])

    def test_parse_21(self):
        self.assertEqual(
            NIPPLES_ENLARGED.parse(
                "reproductive data=No placental scars or embryos. "
                "3 nipples prominent"
            ),
            [Trait(value="enlarged", start=51, end=68)],
        )

    def test_parse_22(self):
        self.assertEqual(
            NIPPLES_ENLARGED.parse("reproductive data=nipple dev: none, no plsc,"),
            [Trait(value="not enlarged", start=18, end=34)],
        )

    def test_parse_23(self):
        self.assertEqual(
            NIPPLES_ENLARGED.parse("reproductive data=nipple dev, 3R+0L=3 plsc ;"), []
        )

    def test_parse_24(self):
        self.assertEqual(
            NIPPLES_ENLARGED.parse(", pelvis slgt sep, nipp med+, no scars,"), []
        )

    def test_parse_25(self):
        self.assertEqual(
            NIPPLES_ENLARGED.parse(
                "reproductive data=Ad. mammery glands developed " "but no nipples"
            ),
            [Trait(value="not enlarged", start=51, end=61)],
        )

    def test_parse_26(self):
        self.assertEqual(
            NIPPLES_ENLARGED.parse(
                "reproductive data=vulva open; no nipples apparent ;"
            ),
            [Trait(value="not enlarged", start=30, end=40)],
        )

    def test_parse_27(self):
        self.assertEqual(
            NIPPLES_ENLARGED.parse(
                "reproductive data=Lactating; clear & enlarged teats ;"
            ),
            [Trait(value="enlarged", start=37, end=51)],
        )

    def test_parse_28(self):
        self.assertEqual(
            NIPPLES_ENLARGED.parse("reproductive data=enlargedNipples ;"),
            [Trait(value="enlarged", start=18, end=33)],
        )

    def test_parse_29(self):
        self.assertEqual(
            NIPPLES_ENLARGED.parse("reproductive data=OEN;"),
            [Trait(value="enlarged", start=18, end=21)],
        )

    def test_parse_30(self):
        self.assertEqual(
            NIPPLES_ENLARGED.parse("reproductive data=OSN;"),
            [Trait(value="not enlarged", start=18, end=21)],
        )
