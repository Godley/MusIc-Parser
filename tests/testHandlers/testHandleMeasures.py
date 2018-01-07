import unittest

from museparse.elements import key, barlinesandmarkers, clef, harmony, part
from museparse.input import mxmlparser
from museparse.tree.piecetree import PieceTree
from museparse.tree.measurenode import MeasureNode


class MeasureTesting(unittest.TestCase):

    def setUp(self):
        self.tags = []
        self.tags.append("measure")
        self.attrs = {"measure": {"number": "1"}, "part": {"id": "P1"}}
        self.chars = {}
        self.handler = mxmlparser.HandleMeasures
        self.piece = PieceTree()
        self.piece.addPart(index="P1", item=part.Part())
        self.part = self.piece.getPart("P1")
        mxmlparser.direction = None
        mxmlparser.note = None
        mxmlparser.expression = None
        self.data = {
            "note": None,
            "direction": None,
            "expression": None,
            "staff_id": 1,
            "voice": 1}

    def tearDown(self):
        self.piece = None


class testHandleMeasures(MeasureTesting):

    def testNoData(self):
        mxmlparser.part_id = None
        self.tags.remove("measure")
        self.attrs.pop("measure")
        self.assertEqual(
            None,
            self.handler(
                self.tags,
                self.attrs,
                self.chars,
                self.piece,
                self.data))

    def testUnrelatedTag(self):
        mxmlparser.part_id = None
        self.tags.remove("measure")
        self.attrs.pop("measure")
        self.tags.append("wibble")
        self.assertEqual(
            None,
            self.handler(
                self.tags,
                self.attrs,
                self.chars,
                self.piece,
                self.data))

    def testMeasureTag(self):
        self.handler(self.tags, self.attrs, None, self.piece, self.data)
        self.assertEqual(
            MeasureNode, type(
                self.piece.getPart("P1").getMeasure(
                    1, 1)))

    def testMeasurePrintTag(self):
        self.tags.append("print")
        self.attrs["print"] = {"new-system": "yes"}
        self.handler(self.tags, self.attrs, None, self.piece, self.data)
        self.assertTrue(
            hasattr(
                self.piece.getPart("P1").getMeasure(
                    1, 1), "newSystem"))

    def testImplicitMeasure(self):
        self.attrs["measure"] = {"number": "1", "implicit": "yes"}
        self.handler(self.tags, self.attrs, None, self.piece, self.data)
        self.assertTrue(
            hasattr(
                self.piece.getPart("P1").getMeasure(
                    1, 1), "partial"))


class testKeySig(MeasureTesting):

    def tearDown(self):
        self.data["staff_id"] = 1

    def testModeTag(self):
        self.tags.append("key")
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)
        self.tags.append("mode")
        self.chars["mode"] = "minor"
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)
        exp_measure = self.piece.getPart("P1").getMeasure(1, 1)
        self.assertIsInstance(exp_measure.GetLastKey(), key.Key)
        self.assertEqual("minor", exp_measure.GetLastKey().mode)

    def testFifthsTag(self):
        self.tags.append("key")
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)
        self.tags.append("fifths")
        self.chars["fifths"] = "3"
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)
        exp_measure = self.piece.getPart("P1").getMeasure(1, 1)
        self.assertIsInstance(exp_measure.GetLastKey(), key.Key)
        self.assertEqual(3, exp_measure.GetLastKey().fifths)

    def testKeySigWithStaffAssignment(self):
        self.tags.append("key")
        self.attrs["key"] = {"number": "2"}
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)
        self.tags.append("fifths")

        self.chars["fifths"] = "3"
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)
        exp_measure = self.piece.getPart("P1").getMeasure(1, 2)
        self.assertIsInstance(exp_measure.GetLastKey(), key.Key)

    def testKeyWithoutStaffAssignment(self):
        self.piece.getPart("P1").addEmptyMeasure(1, 1)
        self.piece.getPart("P1").addEmptyMeasure(1, 2)
        exp_measure = self.piece.getPart("P1").getMeasure(1, 2)
        measure_2 = self.piece.getPart("P1").getMeasure(1, 1)
        self.tags.append("key")
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)
        self.tags.append("fifths")
        self.chars["fifths"] = "3"
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)

        self.assertIsInstance(exp_measure.GetLastKey(), key.Key)
        self.assertIsInstance(measure_2.GetLastKey(), key.Key)


class testMeter(MeasureTesting):

    def testSingleBeatAttrib(self):
        self.tags.append("time")
        self.attrs["time"] = {"symbol": "single-number"}
        self.tags.append("beats")
        self.chars["beats"] = "3"
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)
        exp_measure = self.piece.getPart("P1").getMeasure(1, 1)
        self.assertTrue(hasattr(exp_measure, "meter"))
        self.assertEqual("single-number", exp_measure.meter.style)

    def testBeatTag(self):
        self.tags.append("meter")
        self.tags.append("beats")
        self.chars["beats"] = "4"
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)
        exp_measure = self.piece.getPart("P1").getMeasure(1, 1)
        self.assertTrue(hasattr(exp_measure, "meter"))
        self.assertEqual(4, exp_measure.meter.beats)

    def testBeatTypeTag(self):
        self.tags.append("meter")
        self.tags.append("beat-type")
        self.chars["beat-type"] = "4"
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)
        exp_measure = self.piece.getPart("P1").getMeasure(1, 1)
        self.assertTrue(hasattr(exp_measure, "meter"))
        self.assertEqual(4, exp_measure.meter.type)


class testClef(MeasureTesting):

    def testLineTag(self):
        self.tags.append("clef")
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)
        self.tags.append("line")
        self.chars["line"] = 2
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)
        exp_measure = self.piece.getPart("P1").getMeasure(1, 1)
        self.assertIsInstance(exp_measure.GetLastClef(), clef.Clef)
        self.assertEqual(2, exp_measure.GetLastClef().line)

    def testSignTag(self):
        self.tags.append("clef")
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)
        self.tags.append("sign")
        self.chars["sign"] = "G"
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)
        exp_measure = self.piece.getPart("P1").getMeasure(1, 1)
        self.assertIsInstance(exp_measure.GetLastClef(), clef.Clef)
        self.assertEqual("G", exp_measure.GetLastClef().sign)

    def testClefWithNumber(self):
        self.tags.append("clef")
        self.attrs["clef"] = {"number": "2"}
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)
        self.tags.append("sign")
        self.chars["sign"] = "G"
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)
        exp_measure = self.piece.getPart("P1").getMeasure(1, 2)
        other_measure = self.piece.getPart("P1").getMeasure(1, 1)
        self.assertIsInstance(exp_measure.GetLastClef(), clef.Clef)
        self.assertIsNone(other_measure.GetLastClef())


class testTranspose(MeasureTesting):

    def testTransposeDiatonicTag(self):
        self.tags.append("transpose")
        self.tags.append("diatonic")
        self.chars["diatonic"] = "0"
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)
        exp_measure = self.piece.getPart("P1").getMeasure(1, 1)
        self.assertTrue(hasattr(exp_measure, "transpose"))
        self.assertEqual("0", exp_measure.transpose.diatonic)

    def testTransposeChromaticTag(self):
        self.tags.append("transpose")
        self.tags.append("chromatic")
        self.chars["chromatic"] = "0"
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)
        exp_measure = self.piece.getPart("P1").getMeasure(1, 1)
        self.assertTrue(hasattr(exp_measure, "transpose"))
        self.assertEqual("0", exp_measure.transpose.chromatic)

    def testTransposeOctaveChangeTag(self):
        self.tags.append("transpose")
        self.tags.append("octave-change")
        self.chars["octave-change"] = "1"
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)
        exp_measure = self.piece.getPart("P1").getMeasure(1, 1)
        self.assertTrue(hasattr(exp_measure, "transpose"))
        self.assertEqual("1", exp_measure.transpose.octave)

    def testPrintNoAttribs(self):
        self.tags.append("print")
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)
        exp_measure = self.piece.getPart("P1").getMeasure(1, 1).GetItem()
        self.assertFalse(hasattr(exp_measure, "new-system"))
        self.assertFalse(hasattr(exp_measure, "new-page"))


class testPrint(MeasureTesting):

    def testPrintNewSysAttrib(self):
        self.tags.append("print")
        self.attrs["print"] = {"new-system": "yes"}
        self.handler(self.tags, self.attrs, None, self.piece, self.data)
        exp_measure = self.piece.getPart("P1").getMeasure(1, 1)
        self.assertTrue(hasattr(exp_measure, "newSystem"))
        self.assertTrue(exp_measure.newSystem)

    def testPrintNewPageAttrib(self):
        self.tags.append("print")
        self.attrs["print"] = {"new-page": "yes"}
        self.handler(self.tags, self.attrs, None, self.piece, self.data)
        exp_measure = self.piece.getPart("P1").getMeasure(1, 1)
        self.assertTrue(hasattr(exp_measure, "newPage"))
        self.assertTrue(exp_measure.newPage)

    def testPrintBothAttrib(self):
        self.tags.append("print")
        self.attrs["print"] = {"new-page": "yes", "new-system": "yes"}
        self.handler(self.tags, self.attrs, None, self.piece, self.data)
        exp_measure = self.piece.getPart("P1").getMeasure(1, 1)
        self.assertTrue(hasattr(exp_measure, "newPage"))
        self.assertTrue(exp_measure.newPage)
        self.assertTrue(hasattr(exp_measure, "newSystem"))
        self.assertTrue(exp_measure.newSystem)


class testHarmony(MeasureTesting):

    def setUp(self):
        MeasureTesting.setUp(self)
        self.tags.append("harmony")
        self.data["degree"] = None
        self.data["frame_note"] = None

    def testHarmonyTag(self):
        self.tags.append("harmony")
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)

        self.measure = self.part.getMeasure(1, 1)
        self.assertIsInstance(self.data["direction"], harmony.Harmony)

    def testRootStep(self):
        self.tags.append("root")
        self.tags.append("root-step")
        self.chars["root-step"] = "A"
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)

        self.measure = self.part.getMeasure(1, 1)
        self.assertTrue(hasattr(self.data["direction"], "root"))

    def testRootStepVal(self):
        self.tags.append("root")
        self.tags.append("root-step")
        self.chars["root-step"] = "A"
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)

        self.measure = self.part.getMeasure(1, 1)
        self.assertEqual("A", self.data["direction"].root.step)

    def testRootAlter(self):
        self.tags.append("root")
        self.tags.append("root-alter")
        self.chars["root-alter"] = "1"
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)

        self.measure = self.part.getMeasure(1, 1)
        self.assertEqual("1", self.data["direction"].root.alter)

    def testKindTag(self):
        self.tags.append("kind")
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)

        self.measure = self.part.getMeasure(1, 1)
        self.assertTrue(hasattr(self.data["direction"], "kind"))

    def testKindVal(self):
        self.tags.append("kind")
        self.chars["kind"] = "major"
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)

        self.measure = self.part.getMeasure(1, 1)
        self.assertEqual("major", self.data["direction"].kind.value)

    def testKindAttribs(self):
        self.tags.append("kind")
        self.chars["kind"] = "major"
        self.attrs["kind"] = {
            "text": "6",
            "halign": "center",
            "parenthesis-degrees": "no"}
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)

        self.measure = self.part.getMeasure(1, 1)
        self.assertTrue(hasattr(self.data["direction"].kind, "text"))
        self.assertTrue(hasattr(self.data["direction"].kind, "halign"))
        self.assertTrue(hasattr(self.data["direction"].kind, "parenthesis"))

    def testBassTag(self):
        # because I'm all about that
        self.tags.append("bass")
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)

        self.measure = self.part.getMeasure(1, 1)
        self.assertTrue(hasattr(self.data["direction"], "bass"))

    def testBassStepVal(self):
        self.tags.append("bass")
        self.tags.append("bass-step")
        self.chars["bass-step"] = "D"
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)

        self.measure = self.part.getMeasure(1, 1)
        self.assertEqual("D", self.data["direction"].bass.step)

    def testBassAlter(self):
        self.tags.append("bass")
        self.tags.append("bass-alter")
        self.chars["bass-alter"] = "1"
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)
        self.measure = self.part.getMeasure(1, 1)
        self.assertEqual("1", self.data["direction"].bass.alter)

    def testDegreeTag(self):
        self.tags.append("degree")
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)

        self.measure = self.part.getMeasure(1, 1)
        self.assertEqual(1, len(self.data["direction"].degrees))

    def testDegreeValue(self):
        self.tags.append("degree")
        self.tags.append("degree-value")
        self.chars["degree-value"] = "9"
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)

        self.measure = self.part.getMeasure(1, 1)
        self.assertEqual("9", self.data["direction"].degrees[-1].value)

    def testDegreeAlter(self):
        self.tags.append("degree")
        self.tags.append("degree-alter")
        self.chars["degree-alter"] = "1"
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)

        self.measure = self.part.getMeasure(1, 1)
        self.assertEqual("1", self.data["direction"].degrees[-1].alter)

    def testDegreeType(self):
        self.tags.append("degree")
        self.tags.append("degree-type")
        self.chars["degree-type"] = "add"
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)

        self.measure = self.part.getMeasure(1, 1)
        self.assertEqual("add", self.data["direction"].degrees[-1].type)

    def testDegreeDisplay(self):
        self.tags.append("degree")
        self.tags.append("degree-type")
        self.chars["degree-type"] = "add"
        self.attrs["degree-type"] = {"text": ""}
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)

        self.measure = self.part.getMeasure(1, 1)
        self.assertEqual("", self.data["direction"].degrees[-1].display)

    def testFrame(self):
        self.tags.append("frame")
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)

        self.measure = self.part.getMeasure(1, 1)
        self.assertTrue(hasattr(self.data["direction"], "frame"))

    def testFrameType(self):
        self.tags.append("frame")
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)

        self.measure = self.part.getMeasure(1, 1)
        self.assertIsInstance(self.data["direction"].frame, harmony.Frame)

    def testFirstFret(self):
        self.tags.append("frame")
        self.tags.append("first-fret")
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)

        self.measure = self.part.getMeasure(1, 1)
        self.assertTrue(hasattr(self.data["direction"].frame, "firstFret"))

    def testFirstFretVal(self):
        self.tags.append("frame")
        self.tags.append("first-fret")
        self.chars["first-fret"] = "6"
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)

        self.measure = self.part.getMeasure(1, 1)
        self.assertEqual("6", self.data["direction"].frame.firstFret[0])

    def testFrameStrings(self):
        self.tags.append("frame")
        self.tags.append("frame-strings")
        self.chars["frame-strings"] = "6"
        print("frame_strings")
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)

        self.measure = self.part.getMeasure(1, 1)
        self.assertEqual("6", self.data["direction"].frame.strings)

    def testFrameFrets(self):
        self.tags.append("frame")
        self.tags.append("frame-frets")
        self.chars["frame-frets"] = "5"
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)

        self.measure = self.part.getMeasure(1, 1)
        self.assertEqual("5", self.data["direction"].frame.frets)

    def testFrameNote(self):
        self.tags.append("frame")
        self.tags.append("frame-note")
        self.tags.append("string")
        self.chars["string"] = "1"
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)

        self.measure = self.part.getMeasure(1, 1)
        self.assertEqual(1, len(self.data["direction"].frame.notes))

    def testFrameNoteString(self):
        self.tags.append("frame")
        self.tags.append("frame-note")
        self.tags.append("string")
        self.chars["string"] = "1"
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)

        self.measure = self.part.getMeasure(1, 1)
        self.assertTrue(1 in self.data["direction"].frame.notes)

    def testFrameNoteFret(self):
        self.tags.append("frame")
        self.tags.append("frame-note")
        self.tags.append("string")
        self.chars["string"] = "3"
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)
        self.tags.append("fret")
        self.chars["fret"] = "1"
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)

        self.measure = self.part.getMeasure(1, 1)
        self.assertEqual("1", self.data["direction"].frame.notes[3].fret)

    def testFrameNoteBarre(self):
        self.tags.append("frame")
        self.tags.append("frame-note")
        self.tags.append("string")
        self.chars["string"] = "1"
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)
        self.tags.append("barre")
        self.attrs["barre"] = {"type": "start"}
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)

        self.measure = self.part.getMeasure(1, 1)
        self.assertEqual("start", self.data["direction"].frame.notes[1].barre)

    def testFrameNoteFingering(self):
        self.tags.append("frame")
        self.tags.append("frame-note")
        self.tags.append("string")
        self.chars["string"] = "1"
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)
        self.tags.append("fingering")
        self.chars["fingering"] = "3"
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)

        self.measure = self.part.getMeasure(1, 1)
        self.assertEqual("3", self.data["direction"].frame.notes[1].fingering)


class testBarline(MeasureTesting):

    def setUp(self):
        MeasureTesting.setUp(self)
        self.part.addEmptyMeasure(1, 1)
        self.measure = self.part.getMeasure(1, 1)
        self.handler = mxmlparser.handleBarline
        self.tags.append("barline")
        self.data = {"note": None, "direction": None, "expression": None}
        self.data["staff_id"] = 1
        mxmlparser.last_barline = None

    def testBarline(self):
        self.attrs["barline"] = {"location": "left"}
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)
        self.assertTrue(hasattr(self.measure, "barlines"))
        self.assertIsInstance(self.measure.barlines, dict)

    def testBarlineLocation(self):
        self.attrs["barline"] = {"location": "left"}
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)
        self.assertTrue("left" in self.measure.barlines.keys())
        self.assertIsInstance(
            self.measure.GetBarline("left"),
            barlinesandmarkers.Barline)

    def testBarStyle(self):
        self.attrs["barline"] = {"location": "left"}
        self.tags.append("bar-style")
        self.chars["bar-style"] = "heavy-light"
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)
        self.assertEqual("heavy-light", self.measure.GetBarline("left").style)

    def testRepeat(self):
        self.tags.append("repeat")
        self.attrs["barline"] = {"location": "left"}
        self.attrs["repeat"] = {"direction": "backward"}
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)

        self.assertTrue(hasattr(self.measure.GetBarline("left"), "repeat"))

    def testRepeatVal(self):
        self.tags.append("repeat")
        self.attrs["barline"] = {"location": "left"}
        self.attrs["repeat"] = {"direction": "backward"}

        mxmlparser.last_barline = barlinesandmarkers.Barline(repeat="forward")
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)

        self.assertEqual("backward", self.measure.GetBarline("left").repeat)

    def testRepeatValWhenNoPreviousBar(self):
        self.tags.append("repeat")
        self.attrs["barline"] = {"location": "left"}
        self.attrs["repeat"] = {"direction": "backward"}
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)

        self.assertEqual("backward", self.measure.GetBarline("left").repeat)


class testRepeatBarline(MeasureTesting):

    def setUp(self):
        MeasureTesting.setUp(self)
        self.part.addEmptyMeasure(1, 1)
        self.measure = self.part.getMeasure(1, 1)
        self.handler = mxmlparser.handleBarline
        self.tags.append("barline")
        self.data["staff_id"] = 1
        mxmlparser.last_barline = None
        self.part.addEmptyMeasure(2, 1)
        self.attrs["measure"] = {"number": "2"}
        self.attrs["barline"] = {"location": "right"}
        self.tags.append("ending")
        self.attrs["ending"] = {"number": "1"}
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)
        self.tags.append("repeat")
        self.attrs["repeat"] = {"direction": "backward"}
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)

    def testRepeatValOfNewMeasure(self):
        measure = self.part.getMeasure(2, 1)
        self.assertEqual(
            measure.GetBarline("right").repeat,
            "backward-barline")
