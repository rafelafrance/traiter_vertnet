"""Test ovary size notations."""
# pylint: disable=missing-module-docstring,missing-class-docstring
# pylint: disable=missing-function-docstring,too-many-public-methods
import unittest

from vertnet.parsers.ovaries_size import OVARY_SIZE
from vertnet.pylib.trait import Trait


class TestOvariesSize(unittest.TestCase):
    def test_parse_01(self):
        self.assertEqual(
            OVARY_SIZE.parse("ovaries = 8x5 mm"),
            [Trait(value=[8, 5], units="mm", units_inferred=False, start=0, end=16)],
        )

    def test_parse_02(self):
        self.assertEqual(
            OVARY_SIZE.parse("ovary < 1 x 1 mm"),
            [Trait(value=[1, 1], units="mm", units_inferred=False, start=0, end=16)],
        )

    def test_parse_03(self):
        self.assertEqual(
            OVARY_SIZE.parse("PIT tag #7F7D4D3A36 REMOVAL GRID #7 TRAP 1C"), []
        )

    def test_parse_04(self):
        self.assertEqual(
            OVARY_SIZE.parse(
                "No tail pencil; Mam. gl. enl., 3 emb. L, 5 R. 1 "
                "corpus lut in L ovary, 7 in R.; Enl[?] 8.1 x 3.5"
            ),
            [],
        )

    def test_parse_05(self):
        self.assertEqual(
            OVARY_SIZE.parse(
                "moderate fat, scars 3R, 4L, no embryos "
                "[right ovary listed, left ovary: 4 x 2 mm]"
            ),
            [
                Trait(
                    value=[4, 2],
                    units="mm",
                    units_inferred=False,
                    side="left",
                    start=60,
                    end=80,
                )
            ],
        )

    def test_parse_06(self):
        self.assertEqual(
            OVARY_SIZE.parse("Rt Ovary 2.0x3.5mm, Lft Ovary 2.1x4.0mm."),
            [
                Trait(
                    value=[2, 3.5],
                    units="mm",
                    units_inferred=False,
                    side="rt",
                    start=0,
                    end=18,
                ),
                Trait(
                    value=[2.1, 4],
                    units="mm",
                    units_inferred=False,
                    side="lft",
                    start=20,
                    end=39,
                ),
            ],
        )

    def test_parse_07(self):
        self.assertEqual(
            OVARY_SIZE.parse("ovaries: 20mm X 12mm, 18mm X 9mm."),
            [
                Trait(
                    value=[20, 12],
                    units=["mm", "mm"],
                    units_inferred=False,
                    start=0,
                    end=32,
                ),
                Trait(
                    value=[18, 9],
                    units=["mm", "mm"],
                    units_inferred=False,
                    start=0,
                    end=32,
                ),
            ],
        )

    def test_parse_08(self):
        self.assertEqual(
            OVARY_SIZE.parse("ovaries = 8 mm"),
            [Trait(value=8, units="mm", units_inferred=False, start=0, end=14)],
        )

    def test_parse_09(self):
        self.assertEqual(
            OVARY_SIZE.parse('"gonad length 1":"3.0", "gonad length 2":"2.0",'),
            [
                Trait(
                    value=3,
                    units=None,
                    units_inferred=True,
                    side="1",
                    dimension="length",
                    ambiguous_key=True,
                    start=1,
                    end=21,
                ),
                Trait(
                    value=2,
                    units=None,
                    units_inferred=True,
                    side="2",
                    dimension="length",
                    ambiguous_key=True,
                    start=25,
                    end=45,
                ),
            ],
        )

    def test_parse_10(self):
        self.assertEqual(
            OVARY_SIZE.parse('"gonadLengthInMM":"12", "gonadWidthInMM":"5",'),
            [
                Trait(
                    value=12,
                    units="MM",
                    units_inferred=False,
                    ambiguous_key=True,
                    dimension="length",
                    start=1,
                    end=21,
                ),
                Trait(
                    value=5,
                    units="MM",
                    units_inferred=False,
                    ambiguous_key=True,
                    dimension="width",
                    start=25,
                    end=43,
                ),
            ],
        )

    def test_parse_11(self):
        self.assertEqual(
            OVARY_SIZE.parse(
                "reproductive data=Embryos "
                "L:11x8mm, 12x8mm; R:10x9mm, 11x10mm. Nippl ; right "
                "gonad length=3 mm; left gonad width=2 mm; right gonad "
                "width=2 mm; left gonad length=3 mm"
            ),
            [
                Trait(
                    value=3,
                    units="mm",
                    units_inferred=False,
                    side="right",
                    ambiguous_key=True,
                    dimension="length",
                    start=71,
                    end=94,
                ),
                Trait(
                    value=2,
                    units="mm",
                    units_inferred=False,
                    side="left",
                    ambiguous_key=True,
                    dimension="width",
                    start=96,
                    end=117,
                ),
                Trait(
                    value=2,
                    units="mm",
                    units_inferred=False,
                    side="right",
                    ambiguous_key=True,
                    dimension="width",
                    start=119,
                    end=141,
                ),
                Trait(
                    value=3,
                    units="mm",
                    units_inferred=False,
                    side="left",
                    ambiguous_key=True,
                    dimension="length",
                    start=143,
                    end=165,
                ),
            ],
        )

    def test_parse_12(self):
        self.assertEqual(
            OVARY_SIZE.parse(
                "reproductive data=Embryos "
                "L:11x8mm, 12x8mm; R:10x9mm, 11x10mm. Nippl ;"
            ),
            [],
        )
