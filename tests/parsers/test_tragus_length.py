"""Test tragus length notations."""
# pylint: disable=missing-module-docstring,missing-class-docstring
# pylint: disable=missing-function-docstring,too-many-public-methods
import unittest
from traiter.pylib.util import shorten
from vertnet.pylib.trait import Trait
from vertnet.parsers.tragus_length import TRAGUS_LENGTH


class TestTragusLength(unittest.TestCase):

    def test_parse_01(self):
        self.assertEqual(
            TRAGUS_LENGTH.parse('Tragus 7;'),
            [Trait(
                value=7, units=None, units_inferred=True, start=0, end=8)])

    def test_parse_02(self):
        self.assertEqual(
            TRAGUS_LENGTH.parse('tragus-5 '),
            [Trait(
                value=5, units=None, units_inferred=True, start=0, end=8)])

    def test_parse_03(self):
        self.assertEqual(
            TRAGUS_LENGTH.parse('; tragus length=9 mm;'),
            [Trait(
                value=9, units='mm', units_inferred=False, start=2, end=20)])

    def test_parse_04(self):
        self.assertEqual(
            TRAGUS_LENGTH.parse(
                """{"totalLengthInMM":"94", "tailLengthInMM":"11","""
                """ "hindfootLengthInMM":"15", "earLengthInMM":"17","""
                """ "tragusLengthInMM":"6", "weightInGrams":"34.7" }"""),
            [Trait(
                value=6, units='MM', units_inferred=False,
                start=98, end=118)])

    def test_parse_05(self):
        self.assertEqual(
            TRAGUS_LENGTH.parse("""ADULT; TR 7-FA 37.3; FET8;"""),
            [Trait(value=7, units=None, units_inferred=True, start=7, end=11)])

    def test_parse_06(self):
        self.assertEqual(
            TRAGUS_LENGTH.parse(shorten("""
                sex=male ; unformatted measurements=126-54-10-16-7=18.7; FA 54
                ; hind foot with claw=10 mm; tragus length=7 mm;
                tail length=54 mm; ear from notch=16 mm;
                forearm length=54 mm; total length=126 mm""")),
            [{'start': 92, 'end': 110, 'units': 'mm', 'value': 7.0,
              'units_inferred': False}])

    def test_parse_07(self):
        self.assertEqual(
            TRAGUS_LENGTH.parse(shorten("""
                {"measurements":"78-39-5-14-8(TR)-30(FA)",
                "weightInGrams":"3.5" }""")),
            [{'start': 2, 'end': 40, 'value': 8.0, 'units': 'mm_shorthand',
              'units_inferred': False, 'is_shorthand': True}])
