"""Test embryo count notations."""
# pylint: disable=missing-module-docstring,missing-class-docstring
# pylint: disable=missing-function-docstring,too-many-public-methods
import unittest
from vertnet.pylib.trait import Trait
from vertnet.parsers.embryo_count import EMBRYO_COUNT


class TestEmbryoCount(unittest.TestCase):

    def test_parse_01(self):
        self.assertEqual(
            EMBRYO_COUNT.parse('pregnant; 4 emb'),
            [Trait(value=4, start=10, end=15)])

    def test_parse_02(self):
        self.assertEqual(
            EMBRYO_COUNT.parse('not pregnant; no embs'),
            [Trait(value=0, start=14, end=21)])

    def test_parse_03(self):
        self.assertEqual(
            EMBRYO_COUNT.parse('pregnant; 4 emb 3L 1R'),
            [Trait(value=4, left=3, right=1, start=10, end=21)])

    def test_parse_04(self):
        self.assertEqual(
            EMBRYO_COUNT.parse('embryos 2R-1L'),
            [Trait(value=3, left=1, right=2, start=0, end=13)])

    def test_parse_05(self):
        self.assertEqual(
            EMBRYO_COUNT.parse('embryo of 34402'),
            [])

    def test_parse_06(self):
        self.assertEqual(
            EMBRYO_COUNT.parse('138-62-18-6  12.4g  scars  emb.1R,1L; '),
            [Trait(value=2, left=1, right=1, start=27, end=36)])

    def test_parse_07(self):
        self.assertEqual(
            EMBRYO_COUNT.parse(
                '; reproductive data=embryos: 4 right , 2 left  ;'),
            [Trait(value=6, left=2, right=4, start=20, end=45)])

    def test_parse_08(self):
        self.assertEqual(
            EMBRYO_COUNT.parse(
                '; reproductive data=embryos: 4 right , 2 left  ;'),
            [Trait(value=6, left=2, right=4, start=20, end=45)])

    def test_parse_09(self):
        self.assertEqual(
            EMBRYO_COUNT.parse('7 embryos, 4 male, and 3 female'),
            [Trait(value=7, male=4, female=3, start=0, end=31)])

    def test_parse_10(self):
        self.assertEqual(
            EMBRYO_COUNT.parse('reproductive data=5 embryos (3L, 2R);'),
            [Trait(value=5, left=3, right=2, start=18, end=35)])

    def test_parse_11(self):
        self.assertEqual(
            EMBRYO_COUNT.parse(
                'reproductive data=Vagina open.  4 small embryos.'),
            [Trait(value=4, start=32, end=47)])

    def test_parse_12(self):
        self.assertEqual(
            EMBRYO_COUNT.parse('; 4 emb. x 07 mm, 3L2R", "weight":"23.0"'),
            [Trait(value=4, left=3, right=2, start=2, end=22)])

    def test_parse_13(self):
        self.assertEqual(
            EMBRYO_COUNT.parse('; 3 emb. x 06 mm.",'),
            [Trait(value=3, start=2, end=7)])

    def test_parse_14(self):
        self.assertEqual(
            EMBRYO_COUNT.parse('reproductive data: 3 embryos - 14 mm, 2R/1L;'),
            [Trait(value=3, left=1, right=2, start=19, end=43)])

    def test_parse_15(self):
        self.assertEqual(
            EMBRYO_COUNT.parse('Med. nipples, no scars or embryos, mod. fat'),
            [Trait(value=0, start=14, end=33)])

    def test_parse_16(self):
        self.assertEqual(
            EMBRYO_COUNT.parse('Fetus of AF 25577 (SHEID-99).'),
            [])

    def test_parse_17(self):
        self.assertEqual(
            EMBRYO_COUNT.parse(', 4 fetuses on left, 1 on right'),
            [Trait(value=5, left=4, right=1, start=2, end=31)])

    def test_parse_18(self):
        self.assertEqual(
            EMBRYO_COUNT.parse('This specimen contained 4 fetuses'),
            [Trait(value=4, start=24, end=33)])

    def test_parse_19(self):
        self.assertEqual(
            EMBRYO_COUNT.parse('; age class=fetus'),
            [])

    def test_parse_20(self):
        self.assertEqual(
            EMBRYO_COUNT.parse("ONLY. 3 VERY LARGE FOETI(50).  REC'D FROM."),
            [Trait(value=3, start=6, end=24)])

    def test_parse_21(self):
        self.assertEqual(
            EMBRYO_COUNT.parse(
                "'Foeti: 2R4L=6'; Donator: Dartmouth College Museum."),
            [Trait(value=6, left=4, right=2, start=1, end=12)])

    def test_parse_22(self):
        self.assertEqual(
            EMBRYO_COUNT.parse('Fetus; Cruise #9999; Fetus of LACM 91773'),
            [])

    def test_parse_23(self):
        self.assertEqual(
            EMBRYO_COUNT.parse(
                '; reproductive data=7 near term embryos 5L, 2R)'),
            [Trait(value=7, left=5, right=2, start=20, end=46)])

    def test_parse_24(self):
        self.assertEqual(
            EMBRYO_COUNT.parse('embryos of NK 125721, embryos NK 125726A-D'),
            [])

    def test_parse_25(self):
        self.assertEqual(
            EMBRYO_COUNT.parse('embryos of NK 125721, embryos NK 125726A-D'),
            [])

    def test_parse_26(self):
        self.assertEqual(
            EMBRYO_COUNT.parse('no emb, 155-79-18-13=13.5'),
            [Trait(value=0, start=0, end=6)])

    def test_parse_27(self):
        self.assertEqual(
            EMBRYO_COUNT.parse(
                'pregnant; 1 emb; CR-74; emb W-25; emb WT-4.8'),
            [Trait(value=1, start=10, end=15)])

    def test_parse_28(self):
        self.assertEqual(
            EMBRYO_COUNT.parse(
                'pregnant; 1 emb; CR-516; emb 516-41-210-44; emb WT-2835'),
            [Trait(value=1, start=10, end=15)])

    def test_parse_29(self):
        self.assertEqual(
            EMBRYO_COUNT.parse(
                'no scars, horns R 2 emb x 11, L 4 emb x 11,'),
            [
                Trait(value=2, side='right', start=16, end=23),
                Trait(value=4, side='left', start=30, end=37)])

    def test_parse_30(self):
        self.assertEqual(
            EMBRYO_COUNT.parse('FOUR EMBS, 25MM'),
            [Trait(value=4, start=0, end=9)])

    def test_parse_31(self):
        self.assertEqual(
            EMBRYO_COUNT.parse('182-95-19-13-18 emb. i'),
            [])

    def test_parse_32(self):
        self.assertEqual(
            EMBRYO_COUNT.parse('2 embryo scars left horn, 1 right'),
            [])

    def test_parse_33(self):
        self.assertEqual(
            EMBRYO_COUNT.parse(
                '3 embryos in left horn, 1 in right, crown to rump 25mm'),
            [Trait(value=4, left=3, right=1, start=0, end=34)])

    def test_parse_34(self):
        self.assertEqual(
            EMBRYO_COUNT.parse('2 embryo scars, 1 in each horn, lactating'),
            [])

    def test_parse_35(self):
        self.assertEqual(
            EMBRYO_COUNT.parse('Fetus found in uterus, saved in formalin'),
            [Trait(value=1, start=0, end=11)])

    def test_parse_36(self):
        self.assertEqual(
            EMBRYO_COUNT.parse('Near-term fetus (86.5 cm S.L.)'),
            [Trait(value=1, start=0, end=15)])

    def test_parse_37(self):
        self.assertEqual(
            EMBRYO_COUNT.parse('Pregnant female, 6 near-term embryos.'),
            [Trait(value=6, start=17, end=36)])

    def test_parse_38(self):
        self.assertEqual(
            EMBRYO_COUNT.parse('2 embryos right horn, 3 left, ~9x10mm'),
            [Trait(value=5, left=3, right=2, start=0, end=28)])

    def test_parse_39(self):
        self.assertEqual(
            EMBRYO_COUNT.parse('Fetus on left, 18mm crown to rump.'),
            [Trait(value=1, side='left', start=0, end=13)])

    def test_parse_40(self):
        self.assertEqual(
            EMBRYO_COUNT.parse('3 embryos L side, 1 R. Mammaries developing.'),
            [Trait(value=4, left=3, right=1, start=0, end=21)])

    def test_parse_41(self):
        self.assertEqual(
            EMBRYO_COUNT.parse('corp. lut. 2L, 4R, no scars, embryos 2L, 4R, '
                               'nipples small, moderate fat'),
            [Trait(value=6, left=2, right=4, start=29, end=43)])

    def test_parse_42(self):
        self.assertEqual(
            EMBRYO_COUNT.parse(
                'perforate; 2L 2R emb; CR-9; 1L R emb; mammary'),
            [Trait(value=4, left=2, right=2, start=11, end=20)])

    def test_parse_43(self):
        self.assertEqual(
            EMBRYO_COUNT.parse('Embryos: 5R x 4L c.r. 3 mm.'),
            [Trait(value=9, left=4, right=5, start=0, end=16)])

    def test_parse_44(self):
        self.assertEqual(
            EMBRYO_COUNT.parse('reproductive data=8 3mm. embryos.'),
            [Trait(value=8, start=18, end=32)])

    def test_parse_45(self):
        self.assertEqual(
            EMBRYO_COUNT.parse('reproductive data=mammae (4L, 5R)'),
            [Trait(value=9, left=4, right=5, start=18, end=32)])

    def test_parse_46(self):
        self.assertEqual(
            EMBRYO_COUNT.parse('embs.=1R,!L'),
            [Trait(value=1, right=1, start=0, end=8)])

    def test_parse_47(self):
        self.assertEqual(
            EMBRYO_COUNT.parse('(260)-(150)-37-14  47.6g  embs 1R,1L'),
            [Trait(value=2, left=1, right=1, start=26, end=36)])

    def test_parse_48(self):
        self.assertEqual(
            EMBRYO_COUNT.parse('1 embryo right horn 4x8mm, 1 embryo left horn'),
            [{'end': 14, 'right': 1, 'start': 0, 'value': 1},
             {'end': 40, 'left': 1, 'start': 27, 'value': 1}])

    # def test_parse_49(self):
    #     self.assertEqual(
    #         EMBRYO_COUNT.parse('embs=1R (CR=32 mm), 1L (CR=32&28mm) ;'),
    #         [{'end': 14, 'left': 1,  'right': 1, 'start': 0, 'value': 2}])
