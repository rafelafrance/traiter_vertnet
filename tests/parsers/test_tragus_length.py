"""Test tragus length notations."""
# pylint: disable=missing-module-docstring,missing-class-docstring
# pylint: disable=missing-function-docstring,too-many-public-methods
import unittest
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
