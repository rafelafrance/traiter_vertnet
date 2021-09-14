"""Test vagina state notations."""
# pylint: disable=missing-module-docstring,missing-class-docstring
# pylint: disable=missing-function-docstring,too-many-public-methods
import unittest
from vertnet.pylib.trait import Trait
from vertnet.parsers.vagina_state import VAGINA_STATE


class TestVaginaState(unittest.TestCase):

    def test_parse_01(self):
        self.assertEqual(
            VAGINA_STATE.parse('reproductive data=perf, Pelvis mod. Sep, nipp med.,'),
            [Trait(value='perf', start=0, end=22)])

    def test_parse_02(self):
        self.assertEqual(
            VAGINA_STATE.parse('reproductive data=Very recent parturition. Perforate.'),
            [Trait(value='perforate', start=0, end=52)])

    def test_parse_03(self):
        self.assertEqual(
            VAGINA_STATE.parse('reproductive data=Uterus clear; OV: No CH ;'),
            [Trait(value='ov', start=0, end=34)])

    def test_parse_04(self):
        self.assertEqual(
            VAGINA_STATE.parse('reproductive data=Vag. Open.'),
            [Trait(value='vag. open', start=18, end=27)])

    def test_parse_05(self):
        self.assertEqual(
            VAGINA_STATE.parse('reproductive data=perf, vag. plug, nipp small,'),
            [Trait(value='perf, vag', start=0, end=27)])

    def test_parse_06(self):
        self.assertEqual(
            VAGINA_STATE.parse('reproductive data=OEL PLSC=0'),
            [Trait(value='oel', start=0, end=21)])

    def test_parse_07(self):
        self.assertEqual(
            VAGINA_STATE.parse('reproductive data=imp, lightly healed,'),
            [Trait(value='imp', start=0, end=21)])

    def test_parse_08(self):
        self.assertEqual(
            VAGINA_STATE.parse('reproductive data=vulva closed,'),
            [Trait(value='vulva closed', start=18, end=30)])

    def test_parse_09(self):
        self.assertEqual(
            VAGINA_STATE.parse('reproductive data=CEN, no plsc ;'),
            [Trait(value='cen', start=0, end=21)])
