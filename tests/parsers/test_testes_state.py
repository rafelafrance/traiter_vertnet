"""Test testes state notations."""
# pylint: disable=missing-module-docstring,missing-class-docstring
# pylint: disable=missing-function-docstring,too-many-public-methods
import unittest
from vertnet.pylib.trait import Trait
from vertnet.parsers.testes_state import TESTES_STATE


class TestTestesState(unittest.TestCase):

    def test_parse_01(self):
        self.assertEqual(
            TESTES_STATE.parse(
                'some words reproductive data=No testicles; more words'),
            [Trait(value='no testicles', start=11, end=41)])

    def test_parse_02(self):
        self.assertEqual(
            TESTES_STATE.parse('testes descended'),
            [Trait(value='descended', start=0, end=16)])

    def test_parse_03(self):
        self.assertEqual(
            TESTES_STATE.parse('testes undescended'),
            [Trait(value='undescended', start=0, end=18)])

    def test_parse_04(self):
        self.assertEqual(
            TESTES_STATE.parse('testes undesc.'),
            [Trait(value='undesc', start=0, end=13)])

    def test_parse_05(self):
        self.assertEqual(
            TESTES_STATE.parse('testes undesc'),
            [Trait(value='undesc', start=0, end=13)])

    def test_parse_06(self):
        self.assertEqual(
            TESTES_STATE.parse('testes not fully descended'),
            [Trait(value='not fully descended', start=0, end=26)])

    def test_parse_07(self):
        self.assertEqual(
            TESTES_STATE.parse('testes not-scrotal'),
            [Trait(value='not-scrotal', start=0, end=18)])

    def test_parse_08(self):
        self.assertEqual(
            TESTES_STATE.parse('testes no scrotum'),
            [Trait(value='no scrotum', start=0, end=17)])

    def test_parse_09(self):
        self.assertEqual(
            TESTES_STATE.parse('testis nscr'),
            [Trait(value='nscr', start=0, end=11)])

    def test_parse_10(self):
        self.assertEqual(
            TESTES_STATE.parse('testes ns'),
            [Trait(value='ns', start=0, end=9)])

    def test_parse_11(self):
        self.assertEqual(
            TESTES_STATE.parse('tes undescend.'),
            [Trait(value='undescend', start=0, end=13)])

    def test_parse_12(self):
        self.assertEqual(
            TESTES_STATE.parse('t abdominal'),
            [Trait(value='abdominal', start=0, end=11)])

    def test_parse_13(self):
        self.assertEqual(
            TESTES_STATE.parse('t nscr'),
            [Trait(value='nscr', start=0, end=6)])

    def test_parse_14(self):
        self.assertEqual(
            TESTES_STATE.parse('t ns'),
            [])

    def test_parse_15(self):
        self.assertEqual(
            TESTES_STATE.parse(
                ('hind foot with claw=35 mm; '
                 'reproductive data=Testes partially descended. '
                 'Sperm present.')),
            [Trait(value='partially descended', start=27, end=71)])

    def test_parse_16(self):
        self.assertEqual(
            TESTES_STATE.parse(
                ('sex=male ; reproductive data=testis 5mm, abdominal '
                 '; ear from notch=20 mm; ')),
            [Trait(value='abdominal', start=11, end=50)])

    def test_parse_17(self):
        self.assertEqual(
            TESTES_STATE.parse('tag# 1089; bag# 156; no gonads'),
            [Trait(value='no gonads', ambiguous_key=True, start=21, end=30)])

    def test_parse_18(self):
        self.assertEqual(
            TESTES_STATE.parse(
                'weight=36 g; reproductive data=testes: 11x7 mm (scrotal)'),
            [Trait(value='scrotal', start=13, end=55)])

    def test_parse_19(self):
        self.assertEqual(
            TESTES_STATE.parse('non-scrotal, sem. ves. 14 mm '),
            [Trait(value='non-scrotal', start=0, end=11)])

    def test_parse_20(self):
        self.assertEqual(
            TESTES_STATE.parse(
                ('verbatim preservation date=8 October 1986 ; '
                 'reproductive data=No testicles')),
            [Trait(value='no testicles', start=44, end=74)])

    def test_parse_21(self):
        self.assertEqual(
            TESTES_STATE.parse(
                'weight=53 g; reproductive data=testes decended, T=8x3 ;'),
            [Trait(value='decended', start=13, end=46)])

    def test_parse_22(self):
        self.assertEqual(
            TESTES_STATE.parse(
                'weight=75.6 g; reproductive data=Testes small'),
            [Trait(value='small', start=15, end=45)])

    def test_parse_23(self):
        self.assertEqual(
            TESTES_STATE.parse('weight=75.6 g; reproductive data=small'),
            [Trait(value='small', start=15, end=38)])

    def test_parse_24(self):
        self.assertEqual(
            TESTES_STATE.parse('puncture wound in left abdominal region.'),
            [])

    def test_parse_25(self):
        self.assertEqual(
            TESTES_STATE.parse(' reproductive data=plsc'),
            [])

    def test_parse_26(self):
        self.assertEqual(
            TESTES_STATE.parse(
                'junk before reproductive data=Testes small, not descended'),
            [Trait(value='small, not descended', start=12, end=57)])

    def test_parse_27(self):
        self.assertEqual(
            TESTES_STATE.parse('Mixed woods // TESTES NOT DESCENDED'),
            [Trait(value='not descended', start=15, end=35)])

    def test_parse_28(self):
        self.assertEqual(
            TESTES_STATE.parse('reproductive data=Uteri small, clear'),
            [])

    def test_parse_29(self):
        self.assertEqual(
            TESTES_STATE.parse(
                ('sex=male ; age class=adult ; reproductive data=scrotal ; '
                 'hind foot with claw=32 mm; weight=82 g; weight=78 g; '
                 'weight=87 g; weight=94 g; reproductive data=nonscrotal ; '
                 'sex=male ; sex=male ; reproductive data=nonscrotal ; '
                 'reproductive data=nonscrotal ; sex=male ; hind foot with '
                 'claw=32 mm; hind foot with claw=34 mm; hind foot with '
                 'claw=34 mm; age class=adult ; age class=adult ; '
                 'age class=adult')),
            [Trait(value='scrotal', start=29, end=54),
             Trait(value='nonscrotal', start=136, end=164),
             Trait(value='nonscrotal', start=189, end=217),
             Trait(value='nonscrotal', start=220, end=248)])

    def test_parse_30(self):
        self.assertEqual(
            TESTES_STATE.parse('reproductive data=NS ;'),
            [Trait(value='ns', start=0, end=20)])

    def test_parse_31(self):
        self.assertEqual(
            TESTES_STATE.parse('reproductive data=SCR ;'),
            [Trait(value='scr', start=0, end=21)])

    def test_parse_32(self):
        self.assertEqual(
            TESTES_STATE.parse('; reproductive data=testes = 4x3 mm; '),
            [])

    def test_parse_33(self):
        self.assertEqual(
            TESTES_STATE.parse(
                'Deciduous woods // TESTES DESCENDED, AND ENLARGED'),
            [Trait(value='descended, and enlarged', start=19, end=49)])

    def test_parse_34(self):
        self.assertEqual(
            TESTES_STATE.parse(
                'Testis abd. Collected with 22 cal. pellet rifle.'),
            [Trait(value='abd', start=0, end=10)])

    def test_parse_35(self):
        self.assertEqual(
            TESTES_STATE.parse(
                'reproductive data=test 3.5x2, pt desc, Et not visib,'),
            [Trait(value='pt desc', start=0, end=37)])
