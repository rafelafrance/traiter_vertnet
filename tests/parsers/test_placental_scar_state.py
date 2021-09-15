"""Test placental scar count notations."""
# pylint: disable=missing-module-docstring,missing-class-docstring
# pylint: disable=missing-function-docstring,too-many-public-methods
import unittest
from vertnet.pylib.trait import Trait
from vertnet.parsers.placental_scar_state import PLACENTAL_SCAR_STATE


class TestPlacentalScarCount(unittest.TestCase):
    def test_parse_01(self):
        self.assertEqual(
            PLACENTAL_SCAR_STATE.parse("no emb; lactating; 7 plac scar"),
            [Trait(value="present", start=19, end=30)],
        )

    def test_parse_02(self):
        self.assertEqual(
            PLACENTAL_SCAR_STATE.parse("vagina imperforate; 5 plac scar 3L 2R"),
            [Trait(value="present", start=20, end=37)],
        )

    def test_parse_03(self):
        self.assertEqual(
            PLACENTAL_SCAR_STATE.parse("3 placental scars, 1L, 2R"),
            [Trait(value="present", start=0, end=25)],
        )

    def test_parse_04(self):
        self.assertEqual(
            PLACENTAL_SCAR_STATE.parse("4 plac scar"),
            [Trait(value="present", start=0, end=11)],
        )

    def test_parse_05(self):
        self.assertEqual(
            PLACENTAL_SCAR_STATE.parse("no placental scars"),
            [Trait(value="absent", start=0, end=18)],
        )

    def test_parse_06(self):
        self.assertEqual(
            PLACENTAL_SCAR_STATE.parse("2+1=3 placental scars"),
            [Trait(value="present", start=0, end=21)],
        )

    def test_parse_07(self):
        self.assertEqual(
            PLACENTAL_SCAR_STATE.parse("U:P UTMD placental scar 1 + 2"),
            [Trait(value="present", start=9, end=29)],
        )

    def test_parse_08(self):
        self.assertEqual(
            PLACENTAL_SCAR_STATE.parse("uterus enlarged, scarring"),
            [Trait(value="present", start=17, end=25)],
        )

    def test_parse_09(self):
        self.assertEqual(
            PLACENTAL_SCAR_STATE.parse("VC, no embs, uterine scars"),
            [Trait(value="absent", start=4, end=26)],
        )

    def test_parse_10(self):
        self.assertEqual(
            PLACENTAL_SCAR_STATE.parse("plac scar 1L"),
            [Trait(value="present", start=0, end=12)],
        )

    def test_parse_11(self):
        self.assertEqual(
            PLACENTAL_SCAR_STATE.parse("; 4 faint placental scars"),
            [Trait(value="present", start=2, end=25)],
        )

    def test_parse_12(self):
        self.assertEqual(
            PLACENTAL_SCAR_STATE.parse("5 plac scars: 3(R)&2(L)"),
            [Trait(value="present", start=0, end=22)],
        )

    def test_parse_13(self):
        self.assertEqual(
            PLACENTAL_SCAR_STATE.parse("2 placental scars, 0L, 2R"),
            [Trait(value="present", start=0, end=25)],
        )

    def test_parse_14(self):
        self.assertEqual(
            PLACENTAL_SCAR_STATE.parse("2+1=3 placental scars"),
            [Trait(value="present", start=0, end=21)],
        )

    def test_parse_15(self):
        self.assertEqual(
            PLACENTAL_SCAR_STATE.parse("not breeding, two scars, 1 left, 1 right"),
            [Trait(value="present", start=18, end=40)],
        )

    def test_parse_16(self):
        self.assertEqual(
            PLACENTAL_SCAR_STATE.parse("placental scars 1 + 1, mam tissue"),
            [Trait(value="present", start=0, end=21)],
        )

    def test_parse_17(self):
        self.assertEqual(
            PLACENTAL_SCAR_STATE.parse("2 P-SCAR R, 1 P-SCAR L"),
            [Trait(value="present", start=0, end=22)],
        )

    def test_parse_18(self):
        self.assertEqual(
            PLACENTAL_SCAR_STATE.parse("5 scars: 2lf,3rt"),
            [Trait(value="present", start=0, end=16)],
        )

    def test_parse_19(self):
        self.assertEqual(
            PLACENTAL_SCAR_STATE.parse("lactating, P-SCAR-R 3, P-SCAR-L 2"),
            [Trait(value="present", start=11, end=33)],
        )

    def test_parse_20(self):
        self.assertEqual(
            PLACENTAL_SCAR_STATE.parse("1R,0L plac scar"),
            [Trait(value="present", start=0, end=15)],
        )

    def test_parse_21(self):
        self.assertEqual(
            PLACENTAL_SCAR_STATE.parse("3 pac. scars:1(R)&2(L)"),
            [Trait(value="present", start=0, end=21)],
        )

    def test_parse_22(self):
        self.assertEqual(
            PLACENTAL_SCAR_STATE.parse("plac scar-9; lactating)"),
            [Trait(value="present", start=0, end=11)],
        )

    def test_parse_23(self):
        self.assertEqual(
            PLACENTAL_SCAR_STATE.parse("1 lt. plac. scar, 2 rt emb: CR: 16 mm"),
            [Trait(value="present", start=0, end=22)],
        )

    def test_parse_24(self):
        self.assertEqual(
            PLACENTAL_SCAR_STATE.parse("3+4= 7 placental scars"),
            [Trait(value="present", start=0, end=22)],
        )

    def test_parse_25(self):
        self.assertEqual(
            PLACENTAL_SCAR_STATE.parse("; no embroys or scar"),
            [Trait(value="absent", start=2, end=20)],
        )

    def test_parse_26(self):
        self.assertEqual(
            PLACENTAL_SCAR_STATE.parse("; 3 prominent placental scars"),
            [Trait(value="present", start=2, end=29)],
        )

    def test_parse_27(self):
        self.assertEqual(
            PLACENTAL_SCAR_STATE.parse("VO, pg., 1 embryo (discarded), CRL+28 mm"), []
        )

    def test_parse_28(self):
        self.assertEqual(
            PLACENTAL_SCAR_STATE.parse("L 3 plac scars, R 2 pl. scars;"),
            [Trait(value="present", start=0, end=29)],
        )

    def test_parse_29(self):
        self.assertEqual(
            PLACENTAL_SCAR_STATE.parse(
                "reproductive data=3R, 2L, placental scars;sex=female;"
            ),
            [Trait(value="present", start=18, end=41)],
        )

    def test_parse_30(self):
        self.assertEqual(
            PLACENTAL_SCAR_STATE.parse(
                "reproductive data=Scars - 5 on left, 5 of right"
            ),
            [Trait(value="present", start=18, end=47)],
        )

    def test_parse_31(self):
        self.assertEqual(
            PLACENTAL_SCAR_STATE.parse(
                ";reproductive data=Placental scars-2R; Embryos-1L,"
            ),
            [Trait(value="present", start=19, end=37)],
        )

    def test_parse_32(self):
        self.assertEqual(
            PLACENTAL_SCAR_STATE.parse("no visible placental scarring"),
            [Trait(value="absent", start=0, end=29)],
        )

    def test_parse_33(self):
        self.assertEqual(PLACENTAL_SCAR_STATE.parse("; 1 scar on tail ;"), [])

    def test_parse_34(self):
        self.assertEqual(
            PLACENTAL_SCAR_STATE.parse(
                ", no scars horns R 2 plac scars, L 3 plac scars,"
            ),
            [
                Trait(start=2, end=10, value="absent"),
                Trait(value="present", start=17, end=47),
            ],
        )

    def test_parse_35(self):
        self.assertEqual(
            PLACENTAL_SCAR_STATE.parse(
                "reproductive data=perf, pelvis not sep, nipples large, "
                "horns R+L1.5wide 2+plac. scars,"
            ),
            [Trait(value="present", start=74, end=85)],
        )

    def test_parse_36(self):
        self.assertEqual(
            PLACENTAL_SCAR_STATE.parse(
                "; sex=female ; reproductive data=scars  0R-4L ;"
            ),
            [Trait(value="present", start=33, end=45)],
        )

    def test_parse_37(self):
        self.assertEqual(
            PLACENTAL_SCAR_STATE.parse(
                "SKULL CLEANED AT ILLINOIS STATE MUSEUM OCT 95; "
                "SCAR ABOVE TAIL, EVIDENCE OF PAST INSECT DAMAGE;"
            ),
            [],
        )

    def test_parse_38(self):
        self.assertEqual(
            PLACENTAL_SCAR_STATE.parse("ut horns: R 1 definite scar, L 2+ scars;"),
            [Trait(value="present", start=10, end=39)],
        )

    def test_parse_39(self):
        self.assertEqual(
            PLACENTAL_SCAR_STATE.parse("DINO 14431; placental scars"),
            [Trait(value="present", start=12, end=27)],
        )

    def test_parse_40(self):
        self.assertEqual(
            PLACENTAL_SCAR_STATE.parse(
                '"Note in catalog: same as 135478";Scarritt ' 'Venezuelan Exped."'
            ),
            [],
        )

    def test_parse_41(self):
        self.assertEqual(
            PLACENTAL_SCAR_STATE.parse("5 ut scars, 132-62-20-15=19"),
            [Trait(value="present", start=0, end=10)],
        )

    def test_parse_42(self):
        self.assertEqual(
            PLACENTAL_SCAR_STATE.parse(
                "specimen number AJU 372; P-SCAR-R 5, P-SCAR-L 5"
            ),
            [Trait(value="present", start=25, end=47)],
        )

    def test_parse_43(self):
        self.assertEqual(
            PLACENTAL_SCAR_STATE.parse("Zion 11396; NK 36683; scars/no embs/lact"),
            [Trait(value="present", start=22, end=27)],
        )

    def test_parse_44(self):
        self.assertEqual(
            PLACENTAL_SCAR_STATE.parse(
                "negative for nematodes; skull labeled 14 Nov 57. PSM: "
                "Mamm Puget Sound Museum ID 27461"
            ),
            [],
        )

    def test_parse_45(self):
        self.assertEqual(
            PLACENTAL_SCAR_STATE.parse(
                "born in lab on Sept 3 to 7 '56; placed in sep. cage 28 "
                "Sept 56; skull labeled 23 Jan 57"
            ),
            [],
        )

    def test_parse_46(self):
        self.assertEqual(
            PLACENTAL_SCAR_STATE.parse("H,K,L,L,S; UTERINE SCARS=2R"),
            [Trait(value="present", start=11, end=27)],
        )

    def test_parse_47(self):
        self.assertEqual(
            PLACENTAL_SCAR_STATE.parse("no embryonic scars 360-40-125-68 1800g"),
            [Trait(value="absent", start=0, end=18)],
        )

    def test_parse_48(self):
        self.assertEqual(
            PLACENTAL_SCAR_STATE.parse("scars  emb.1R,1L;"),
            [Trait(value="present", start=0, end=5)],
        )

    def test_parse_49(self):
        self.assertEqual(
            PLACENTAL_SCAR_STATE.parse("fat=2; lactating; 14 embryo scars"),
            [Trait(value="present", start=18, end=33)],
        )

    def test_parse_50(self):
        self.assertEqual(
            PLACENTAL_SCAR_STATE.parse("3 scars left, 3 right; lactating."),
            [Trait(value="present", start=0, end=21)],
        )

    def test_parse_51(self):
        self.assertEqual(
            PLACENTAL_SCAR_STATE.parse("Uterine scars: 1 L, 3 R."),
            [Trait(value="present", start=0, end=23)],
        )

    def test_parse_52(self):
        self.assertEqual(
            PLACENTAL_SCAR_STATE.parse("scars: 2R, 2L, no embryos"),
            [Trait(value="present", start=0, end=13)],
        )

    def test_parse_53(self):
        self.assertEqual(
            PLACENTAL_SCAR_STATE.parse("corp. lut. 4L, 3R, scars 3L, 3R, no embryos"),
            [Trait(value="present", start=15, end=27)],
        )

    def test_parse_55(self):
        self.assertEqual(
            PLACENTAL_SCAR_STATE.parse(
                "no embryos, scars 2R, 3L, corp. lut. 2R, 4L, nipples"
            ),
            [Trait(value="present", start=12, end=24)],
        )

    def test_parse_56(self):
        self.assertEqual(
            PLACENTAL_SCAR_STATE.parse("reproductive data=nip small, no plsc ; "),
            [Trait(value="absent", start=29, end=36)],
        )
