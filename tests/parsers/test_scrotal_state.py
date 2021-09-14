"""Test scrotal state notations."""
# pylint: disable=missing-module-docstring,missing-class-docstring
# pylint: disable=missing-function-docstring,too-many-public-methods
import unittest
from vertnet.pylib.trait import Trait
from vertnet.parsers.scrotal_state import SCROTAL_STATE


class TestScrotalState(unittest.TestCase):

    def test_parse_01(self):
        self.assertEqual(
            SCROTAL_STATE.parse('testes not-scrotal'),
            [Trait(value='testes not-scrotal', start=0, end=18)])

    def test_parse_02(self):
        self.assertEqual(
            SCROTAL_STATE.parse('testes no scrotum'),
            [Trait(value='testes no scrotum', start=0, end=17)])

    def test_parse_03(self):
        self.assertEqual(
            SCROTAL_STATE.parse('testis nscr'),
            [Trait(value='testis nscr', start=0, end=11)])

    def test_parse_04(self):
        self.assertEqual(
            SCROTAL_STATE.parse('testes ns'),
            [Trait(value='testes ns', start=0, end=9)])

    def test_parse_05(self):
        self.assertEqual(
            SCROTAL_STATE.parse('t nscr'),
            [Trait(value='t nscr', start=0, end=6)])

    def test_parse_06(self):
        self.assertEqual(
            SCROTAL_STATE.parse('t ns'),
            [{'end': 4, 'start': 0, 'value': 't ns'}])

    def test_parse_07(self):
        self.assertEqual(
            SCROTAL_STATE.parse(
                'weight=36 g; reproductive data=testes: 11x7 mm (scrotal)'),
            [Trait(value='scrotal', start=48, end=55)])

    def test_parse_08(self):
        self.assertEqual(
            SCROTAL_STATE.parse('non-scrotal, sem. ves. 14 mm '),
            [Trait(value='non-scrotal', start=0, end=11)])

    def test_parse_09(self):
        self.assertEqual(
            SCROTAL_STATE.parse(
                ('sex=male ; age class=adult ; reproductive data=scrotal ; '
                 'hind foot with claw=32 mm; weight=82 g; weight=78 g; '
                 'weight=87 g; weight=94 g; reproductive data=nonscrotal ; '
                 'sex=male ; sex=male ; reproductive data=nonscrotal ; '
                 'reproductive data=nonscrotal ; sex=male ; hind foot with '
                 'claw=32 mm; hind foot with claw=34 mm; hind foot with '
                 'claw=34 mm; age class=adult ; age class=adult ; '
                 'age class=adult')),
            [Trait(value='scrotal', start=47, end=54),
             Trait(value='nonscrotal', start=154, end=164),
             Trait(value='nonscrotal', start=207, end=217),
             Trait(value='nonscrotal', start=238, end=248)])

    def test_parse_10(self):
        self.assertEqual(
            SCROTAL_STATE.parse('reproductive data=NS ;'),
            [Trait(value='ns', start=0, end=20)])

    def test_parse_11(self):
        self.assertEqual(
            SCROTAL_STATE.parse('reproductive data=SCR ;'),
            [Trait(value='scr', start=18, end=21)])
