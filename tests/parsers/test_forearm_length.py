"""Test forearm length notations."""
# pylint: disable=missing-module-docstring,missing-class-docstring
# pylint: disable=missing-function-docstring,too-many-public-methods
import unittest
from vertnet.pylib.trait import Trait
from vertnet.parsers.forearm_length import FOREARM_LENGTH


class TestForearmLength(unittest.TestCase):

    def test_parse_01(self):
        self.assertEqual(
            FOREARM_LENGTH.parse('Forearm 33;'),
            [Trait(
                value=33, units=None, units_inferred=True, start=0, end=10)])

    def test_parse_02(self):
        self.assertEqual(
            FOREARM_LENGTH.parse('For.A. 33;'),
            [Trait(
                value=33, units=None, units_inferred=True, start=0, end=9)])

    def test_parse_03(self):
        self.assertEqual(
            FOREARM_LENGTH.parse('Forea. 33;'),
            [Trait(
                value=33, units=None, units_inferred=True, start=0, end=9)])

    def test_parse_04(self):
        self.assertEqual(
            FOREARM_LENGTH.parse(
                'unformatted measurements=67-27.1-5.2-9.2-3.9=x, FA 29.3'),
            [
                Trait(
                    value=3.9, units='mm_shorthand', units_inferred=False,
                    is_shorthand=True, start=12, end=46),
                Trait(
                    value=29.3, units=None, units_inferred=True,
                    start=48, end=55),
                ])

    def test_parse_05(self):
        self.assertEqual(
            FOREARM_LENGTH.parse('Forearm- 90'),
            [Trait(
                value=90, units=None, units_inferred=True, start=0, end=11)])

    def test_parse_06(self):
        self.assertEqual(
            FOREARM_LENGTH.parse(
                'Note in catalog: Mus. SW Biol. NK 30009; 91-0-17-22-[62] x'),
            [Trait(
                value=62, estimated_value=True, units='mm_shorthand',
                units_inferred=False, is_shorthand=True, start=41, end=58)])

    def test_parse_07(self):
        self.assertEqual(
            FOREARM_LENGTH.parse(
                '{"measurements":"82-34-8-13-32(fa)", "weightInGrams":"8.0"}'),
            [Trait(
                value=32, units='mm_shorthand',
                units_inferred=False, is_shorthand=True, start=2, end=34)])

    def test_parse_08(self):
        self.assertEqual(
            FOREARM_LENGTH.parse(
                '{"measurements":"44.0 (FA)" }'),
            [Trait(
                value=44, units=None, units_inferred=True, start=17, end=25)])

    def test_parse_09(self):
        self.assertEqual(
            FOREARM_LENGTH.parse(
                '{"ADULT;  TR 7-FA 37.3; FET8;'),
            [Trait(
                value=37.3, units=None, units_inferred=True,
                start=15, end=22)])

    def test_parse_10(self):
        self.assertEqual(
            FOREARM_LENGTH.parse(
                'Big brown bat, tragus L.-7mm, forearm L.-28mm.'),
            [Trait(value=28.0, units='mm', units_inferred=False,
                   start=30, end=45)])
