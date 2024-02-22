"""Test embryo count notations."""
# pylint: disable=missing-module-docstring,missing-class-docstring
# pylint: disable=missing-function-docstring,too-many-public-methods
import unittest

from vertnet.parsers.embryo_count import EMBRYO_COUNT
from vertnet.pylib.trait import Trait


class TestEmbryoCount(unittest.TestCase):
    def test_parse_01(self):
        self.assertEqual(
            EMBRYO_COUNT.parse("pregnant; 4 emb"), [Trait(value=4, start=10, end=15)]
        )

    def test_parse_02(self):
        self.assertEqual(
            EMBRYO_COUNT.parse("not pregnant; no embs"),
            [{"end": 12, "start": 0, "value": 0}, {"end": 21, "start": 14, "value": 0}],
        )

    def test_parse_03(self):
        self.assertEqual(
            EMBRYO_COUNT.parse("pregnant; 4 emb 3L 1R"),
            [Trait(value=4, left=3, right=1, start=10, end=21)],
        )

    def test_parse_04(self):
        self.assertEqual(
            EMBRYO_COUNT.parse("embryos 2R-1L"),
            [Trait(value=3, left=1, right=2, start=0, end=13)],
        )

    def test_parse_05(self):
        self.assertEqual(EMBRYO_COUNT.parse("embryo of 34402"), [])

    def test_parse_06(self):
        self.assertEqual(
            EMBRYO_COUNT.parse("138-62-18-6  12.4g  scars  emb.1R,1L; "),
            [Trait(value=2, left=1, right=1, start=27, end=36)],
        )

    def test_parse_07(self):
        self.assertEqual(
            EMBRYO_COUNT.parse("; reproductive data=embryos: 4 right , 2 left  ;"),
            [Trait(value=6, left=2, right=4, start=20, end=45)],
        )

    def test_parse_08(self):
        self.assertEqual(
            EMBRYO_COUNT.parse("; reproductive data=embryos: 4 right , 2 left  ;"),
            [Trait(value=6, left=2, right=4, start=20, end=45)],
        )

    def test_parse_09(self):
        self.assertEqual(
            EMBRYO_COUNT.parse("7 embryos, 4 male, and 3 female"),
            [Trait(value=7, male=4, female=3, start=0, end=31)],
        )

    def test_parse_10(self):
        self.assertEqual(
            EMBRYO_COUNT.parse("reproductive data=5 embryos (3L, 2R);"),
            [Trait(value=5, left=3, right=2, start=18, end=35)],
        )

    def test_parse_11(self):
        self.assertEqual(
            EMBRYO_COUNT.parse("reproductive data=Vagina open.  4 small embryos."),
            [Trait(value=4, start=32, end=47)],
        )

    def test_parse_12(self):
        self.assertEqual(
            EMBRYO_COUNT.parse('; 4 emb. x 07 mm, 3L2R", "weight":"23.0"'),
            [Trait(value=5, left=3, right=2, start=2, end=22)],
        )

    def test_parse_13(self):
        self.assertEqual(
            EMBRYO_COUNT.parse('; 3 emb. x 06 mm.",'), [Trait(value=3, start=2, end=7)]
        )

    def test_parse_14(self):
        self.assertEqual(
            EMBRYO_COUNT.parse("reproductive data: 3 embryos - 14 mm, 2R/1L;"),
            [Trait(value=3, left=1, right=2, start=19, end=43)],
        )

    def test_parse_15(self):
        self.assertEqual(
            EMBRYO_COUNT.parse("Med. nipples, no scars or embryos, mod. fat"),
            [Trait(value=0, start=14, end=33)],
        )

    def test_parse_16(self):
        self.assertEqual(EMBRYO_COUNT.parse("Fetus of AF 25577 (SHEID-99)."), [])

    def test_parse_17(self):
        self.assertEqual(
            EMBRYO_COUNT.parse(", 4 fetuses on left, 1 on right"),
            [Trait(value=5, left=4, right=1, start=2, end=31)],
        )

    def test_parse_18(self):
        self.assertEqual(
            EMBRYO_COUNT.parse("This specimen contained 4 fetuses"),
            [Trait(value=4, start=24, end=33)],
        )

    def test_parse_19(self):
        self.assertEqual(EMBRYO_COUNT.parse("; age class=fetus"), [])

    def test_parse_20(self):
        self.assertEqual(
            EMBRYO_COUNT.parse("ONLY. 3 VERY LARGE FOETI(50).  REC'D FROM."),
            [Trait(value=3, start=6, end=24)],
        )

    def test_parse_21(self):
        self.assertEqual(
            EMBRYO_COUNT.parse("Foeti: 2R4L=6; Donator: Dartmouth College Museum."),
            [Trait(value=6, left=4, right=2, start=0, end=13)],
        )

    def test_parse_22(self):
        self.assertEqual(
            EMBRYO_COUNT.parse("Fetus; Cruise #9999; Fetus of LACM 91773"), []
        )

    def test_parse_23(self):
        self.assertEqual(
            EMBRYO_COUNT.parse("; reproductive data=7 near term embryos 5L, 2R)"),
            [Trait(value=7, left=5, right=2, start=20, end=46)],
        )

    def test_parse_24(self):
        self.assertEqual(
            EMBRYO_COUNT.parse("embryos of NK 125721, embryos NK 125726A-D"), []
        )

    def test_parse_25(self):
        self.assertEqual(
            EMBRYO_COUNT.parse("embryos of NK 125721, embryos NK 125726A-D"), []
        )

    def test_parse_26(self):
        self.assertEqual(
            EMBRYO_COUNT.parse("no emb, 155-79-18-13=13.5"),
            [Trait(value=0, start=0, end=6)],
        )

    def test_parse_27(self):
        self.assertEqual(
            EMBRYO_COUNT.parse("pregnant; 1 emb; CR-74; emb W-25; emb WT-4.8"),
            [Trait(value=1, start=10, end=15)],
        )

    def test_parse_28(self):
        self.assertEqual(
            EMBRYO_COUNT.parse(
                "pregnant; 1 emb; CR-516; emb 516-41-210-44; emb WT-2835"
            ),
            [Trait(value=1, start=10, end=15)],
        )

    def test_parse_29(self):
        self.assertEqual(
            EMBRYO_COUNT.parse("no scars, horns R 2 emb x 11, L 4 emb x 11,"),
            [Trait(value=6, left=4, right=2, start=16, end=37)],
        )

    def test_parse_30(self):
        self.assertEqual(
            EMBRYO_COUNT.parse("FOUR EMBS, 25MM"), [Trait(value=4, start=0, end=9)]
        )

    def test_parse_31(self):
        self.assertEqual(EMBRYO_COUNT.parse("182-95-19-13-18 emb. i"), [])

    def test_parse_32(self):
        self.assertEqual(EMBRYO_COUNT.parse("2 embryo scars left horn, 1 right"), [])

    def test_parse_33(self):
        self.assertEqual(
            EMBRYO_COUNT.parse(
                "3 embryos in left horn, 1 in right, crown to rump 25mm"
            ),
            [Trait(value=4, left=3, right=1, start=0, end=34)],
        )

    def test_parse_34(self):
        self.assertEqual(
            EMBRYO_COUNT.parse("2 embryo scars, 1 in each horn, lactating"), []
        )

    def test_parse_35(self):
        self.assertEqual(
            EMBRYO_COUNT.parse("Fetus found in uterus, saved in formalin"),
            [Trait(value=1, start=0, end=11)],
        )

    def test_parse_36(self):
        self.assertEqual(
            EMBRYO_COUNT.parse("Near-term fetus (86.5 cm S.L.)"),
            [Trait(value=1, start=0, end=15)],
        )

    def test_parse_37(self):
        self.assertEqual(
            EMBRYO_COUNT.parse("Pregnant female, 6 near-term embryos."),
            [Trait(value=6, start=17, end=36)],
        )

    def test_parse_38(self):
        self.assertEqual(
            EMBRYO_COUNT.parse("2 embryos right horn, 3 left, ~9x10mm"),
            [Trait(value=5, left=3, right=2, start=0, end=28)],
        )

    def test_parse_39(self):
        self.assertEqual(
            EMBRYO_COUNT.parse("Fetus on left, 18mm crown to rump."),
            [Trait(value=1, side="left", start=0, end=13)],
        )

    def test_parse_40(self):
        self.assertEqual(
            EMBRYO_COUNT.parse("3 embryos L side, 1 R. Mammaries developing."),
            [Trait(value=4, left=3, right=1, start=0, end=21)],
        )

    def test_parse_41(self):
        self.assertEqual(
            EMBRYO_COUNT.parse(
                "corp. lut. 2L, 4R, no scars, embryos 2L, 4R, "
                "nipples small, moderate fat"
            ),
            [Trait(value=6, left=2, right=4, start=29, end=43)],
        )

    def test_parse_42(self):
        self.assertEqual(
            EMBRYO_COUNT.parse("perforate; 2L 2R emb; CR-9; 1L R emb; mammary"),
            [Trait(value=4, left=2, right=2, start=11, end=20)],
        )

    def test_parse_43(self):
        self.assertEqual(
            EMBRYO_COUNT.parse("Embryos: 5R x 4L c.r. 3 mm."),
            [Trait(value=9, left=4, right=5, start=0, end=16)],
        )

    def test_parse_44(self):
        self.assertEqual(
            EMBRYO_COUNT.parse("reproductive data=8 3mm. embryos."),
            [Trait(value=8, start=18, end=32)],
        )

    def test_parse_45(self):
        self.assertEqual(
            EMBRYO_COUNT.parse("reproductive data=mammae (4L, 5R)"),
            [Trait(value=9, left=4, right=5, start=0, end=32)],
        )

    def test_parse_46(self):
        self.assertEqual(
            EMBRYO_COUNT.parse("embs.=1R,!L"),
            [Trait(value=1, left=1, right=1, start=0, end=11)],
        )

    def test_parse_47(self):
        self.assertEqual(
            EMBRYO_COUNT.parse("(260)-(150)-37-14  47.6g  embs 1R,1L"),
            [Trait(value=2, left=1, right=1, start=26, end=36)],
        )

    def test_parse_48(self):
        self.assertEqual(
            EMBRYO_COUNT.parse("1 embryo right horn 4x8mm, 1 embryo left horn"),
            [
                {"end": 14, "right": 1, "start": 0, "value": 1},
                {"end": 40, "left": 1, "start": 27, "value": 1},
            ],
        )

    def test_parse_49(self):
        self.assertEqual(
            EMBRYO_COUNT.parse("embs=1R (CR=32 mm), 1L (CR=32&28mm) ;"),
            [{"end": 22, "left": 1, "right": 1, "start": 0, "value": 2}],
        )

    def test_parse_50(self):
        self.assertEqual(
            EMBRYO_COUNT.parse("reproductive data=embryos left:3 right:3 ;"),
            [{"end": 40, "left": 3, "right": 3, "start": 18, "value": 6}],
        )

    def test_parse_51(self):
        self.assertEqual(
            EMBRYO_COUNT.parse(
                "R horn 5embsx18mm, L horn 1 resorb embx5mm, 1embx18mm; "
            ),
            [
                {"end": 27, "left": 1, "right": 5, "start": 0, "value": 6},
                {"end": 48, "start": 44, "value": 1},
            ],
        )

    def test_parse_52(self):
        self.assertEqual(
            EMBRYO_COUNT.parse("emb 5x21 (R2 L3),"),
            [{"end": 15, "left": 3, "right": 2, "start": 0, "value": 5}],
        )

    def test_parse_53(self):
        self.assertEqual(
            EMBRYO_COUNT.parse("emb 1x13( R), 1+ pl sc (L),"),
            [{"end": 11, "right": 1, "start": 0, "value": 1}],
        )

    def test_parse_54(self):
        self.assertEqual(
            EMBRYO_COUNT.parse("reproductive data=3 large, 20mm embryos: 2R, 1L."),
            [{"end": 47, "left": 1, "right": 2, "start": 32, "value": 3}],
        )

    def test_parse_55(self):
        self.assertEqual(
            EMBRYO_COUNT.parse("reproductive data=5 3mm embryos: 1R, 4L"),
            [{"end": 39, "left": 4, "right": 1, "start": 18, "value": 5}],
        )

    def test_parse_56(self):
        self.assertEqual(
            EMBRYO_COUNT.parse("5 3mm embyros: 1R, 4L"),
            [{"end": 21, "left": 4, "right": 1, "start": 0, "value": 5}],
        )

    def test_parse_57(self):
        self.assertEqual(
            EMBRYO_COUNT.parse(
                """vulva w/sm blood clot; R horn 2 mmx2.5 mm,
                L 1 emb x 3 mm and 1 emb 2.5 mm;"""
            ),
            [
                {"end": 66, "start": 61, "value": 1},
                {"end": 83, "start": 78, "value": 1},
            ],
        )

    def test_parse_58(self):
        self.assertEqual(
            EMBRYO_COUNT.parse("2 embryos each side (4 total), 3x4mm"),
            [{"end": 19, "left": 2, "right": 2, "start": 0, "value": 4}],
        )

    def test_parse_59(self):
        self.assertEqual(
            EMBRYO_COUNT.parse("reproductive data=2Rx1Lx23 mm fetuses"),
            [{"end": 24, "left": 1, "right": 2, "start": 0, "value": 3}],
        )

    def test_parse_60(self):
        self.assertEqual(
            EMBRYO_COUNT.parse("VC, R2, L3=19, embryos saved"),
            [{"end": 22, "left": 3, "right": 2, "start": 4, "value": 5}],
        )

    def test_parse_61(self):
        self.assertEqual(
            EMBRYO_COUNT.parse("VO, mamm. lg., 4L, CRL=26, embryos saved"),
            [{"end": 34, "left": 4, "start": 15, "value": 4}],
        )

    def test_parse_62(self):
        self.assertEqual(
            EMBRYO_COUNT.parse("corpora lutea: L-4, R-5; embryos: L-2, R-3 (5x3mm)"),
            [{"end": 42, "left": 2, "right": 3, "start": 25, "value": 5}],
        )

    def test_parse_63(self):
        self.assertEqual(
            EMBRYO_COUNT.parse("Pregnant with 4 embryos (rt = 1, lt = 3;"),
            [{"end": 39, "left": 3, "right": 1, "start": 14, "value": 4}],
        )

    def test_parse_64(self):
        self.assertEqual(
            EMBRYO_COUNT.parse("RBS 4029; EMB-R 2, EMB-L 3, CR 8 mm"),
            [{"end": 26, "left": 3, "right": 2, "start": 10, "value": 5}],
        )

    def test_parse_65(self):
        self.assertEqual(
            EMBRYO_COUNT.parse("reproductive data=4 2.5mm embryos"),
            [{"end": 33, "start": 18, "value": 4}],
        )

    def test_parse_66(self):
        self.assertEqual(
            EMBRYO_COUNT.parse("reproductive data=Emb = 4 : CR = 17mm : 2R x 2L"),
            [{"end": 47, "left": 2, "right": 2, "start": 18, "value": 4}],
        )

    def test_parse_67(self):
        self.assertEqual(
            EMBRYO_COUNT.parse("reproductive data=3 embryos (3R, 1L)"),
            [{"end": 35, "left": 1, "right": 3, "start": 18, "value": 4}],
        )

    # def test_parse_68(self):
    #     self.assertEqual(
    #         EMBRYO_COUNT.parse("Embryos (R2, L4, 10mm)."),
    #         [{"end": 35, "left": 1, "right": 3, "start": 18, "value": 4}],
    #     )
