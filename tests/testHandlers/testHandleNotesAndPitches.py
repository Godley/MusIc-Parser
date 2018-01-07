import unittest

from museparse.tree.piecetree import PieceTree
from museparse.elements import piece, note, part
from museparse.input import mxmlparser


class notes(unittest.TestCase):

    def setUp(self):
        self.tags = ["note"]
        self.chars = {}
        self.attrs = {"part": {"id": "P1"}, "measure": {"number": "1"}}
        self.handler = mxmlparser.CreateNote
        mxmlparser.part_id = "P1"
        mxmlparser.measure_id = 1
        self.piece = PieceTree()
        self.piece.addPart(part.Part(), index="P1")
        self.piece.getPart("P1").addEmptyMeasure(1, 1)
        self.data = {
            "note": None,
            "direction": None,
            "expression": None,
            "staff_id": 1}

    def copy(self):
        pass


class testCreateNoteHandler(notes):

    def setUp(self):
        if isinstance(self, testCreateNoteHandler):
            self.tags = ["note"]
        notes.setUp(self)

    def testNoTags(self):
        self.tags.remove("note")
        self.attrs = {}
        self.assertEqual(
            None,
            self.handler(
                self.tags,
                self.attrs,
                self.chars,
                self.piece,
                self.data),
            "ERROR: 0 tags should do nothing in method CreateNote in testNoData")

    def testIrrelevantTag(self):
        self.tags.remove("note")
        self.attrs = {}
        self.tags.append("hello")
        self.assertEqual(
            None,
            self.handler(
                self.tags,
                self.attrs,
                self.chars,
                self.piece,
                self.data),
            "ERROR: irrelevant tags should get nothing from method CreateNote in testIrrelevantTags")

    def testNoteTag(self):
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)
        self.copy()
        self.assertIsInstance(self.data["note"], note.Note)

    def testNoteChordTag(self):
        self.tags.append("chord")
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)
        self.copy()
        self.assertTrue(hasattr(self.data["note"], "chord"))
# deprecated method of handling: not sure how to test this now? it's done at parser level rather than handler level
    # def testNoteChordTagAffectsPreviousNote(self):
    #     self.tags.append("chord")
    #     mxmlparser.notes[1] = []
    #     mxmlparser.notes[1].append(note.Note())
    #     self.handler(self.tags,self.attrs,self.chars,self.piece, self.data)
    #     self.assertTrue(hasattr(mxmlparser.notes[1][len(mxmlparser.notes[1])-2], "chord"))

    def testRestTag(self):
        self.tags.append("rest")
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)
        self.assertTrue(hasattr(self.data["note"], "rest"))
        self.assertEqual(True, self.data["note"].rest)

    def testRestMeasure(self):
        self.tags.append("rest")
        self.attrs["rest"] = {"measure": "yes"}
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)
        self.assertTrue(hasattr(self.data["note"], "measureRest"))
        self.assertEqual(True, self.data["note"].measureRest)

    def testCueTag(self):
        self.tags.append("cue")
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)
        self.assertTrue(hasattr(self.data["note"], "cue"))

    def testGraceTag(self):
        self.tags.append("grace")
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)
        self.assertIsInstance(
            self.data["note"].search(
                note.GraceNote),
            note.GraceNote)

    def testGraceIsFirst(self):
        self.tags.append("grace")
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)
        self.assertTrue(self.data["note"].search(note.GraceNote).first)

    def testDurationTag(self):
        self.tags.append("duration")
        self.chars["duration"] = "8"
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)
        self.assertTrue(
            hasattr(
                self.data["note"],
                "duration"),
            "ERROR: note should have duration attrib")
        self.assertEqual(
            8,
            self.data["note"].duration,
            "ERROR: note duration set incorrectly")

    def testTypeTag(self):
        self.tags.append("type")
        self.chars["type"] = "eighth"
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)
        self.assertTrue(hasattr(self.data["note"], "val_type"))
        self.assertEqual(8, self.data["note"].duration)

    def testDotTag(self):
        self.tags.append("dot")
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)
        self.assertEqual(self.data["note"].dots, 1)

    def testDoubleDot(self):
        self.tags.append("dot")
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)
        self.tags.append("dot")
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)
        self.assertEqual(self.data["note"].dots, 2)

    def testTieTag(self):
        self.tags.append("tie")
        self.attrs["tie"] = {"type": "start"}
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)
        expected = self.data["note"]
        self.assertEqual(1, len(self.data["note"].ties))
        self.assertEqual("start", expected.ties[-1].type)

    def testStemTag(self):
        self.tags.append("stem")
        self.chars["stem"] = "up"
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)
        note = self.data["note"]
        self.assertTrue(
            hasattr(
                note,
                "stem"),
            "ERROR: stem attrib not added to note")
        self.assertEqual(note.Stem, type(note.stem),
                         "ERROR: stem not of type Stem")
        self.assertEqual(
            "up",
            note.stem.type,
            "ERROR: stem type value incorrect")

    def testBeamTag(self):
        self.tags.append("beam")
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)
        self.assertTrue(hasattr(self.data["note"], "beams"))
        self.assertIsInstance(self.data["note"].beams[0], note.Beam)

    def testBeamType(self):
        self.tags.append("beam")
        self.chars["beam"] = "begin"
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)
        self.assertTrue(hasattr(self.data["note"].beams[0], "type"))
        self.assertEqual("begin", self.data["note"].beams[0].type)

    def testBeamAttrs(self):
        self.tags.append("beam")
        self.chars["beam"] = "begin"
        self.attrs["beam"] = {"number": "1"}
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)
        self.assertTrue(1 in self.data["note"].beams)

    def testAccidental(self):
        self.tags.append("accidental")
        self.chars["accidental"] = "sharp"
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)
        self.assertTrue(hasattr(self.data["note"], "pitch"))
        self.assertTrue(hasattr(self.data["note"].pitch, "accidental"))


class pitchin(unittest.TestCase):

    def setUp(self):
        self.tags = ["note", "pitch"]
        self.attrs = {}
        self.chars = {}

        mxmlparser.part_id = "P1"
        mxmlparser.measure_id = 1
        self.handler = mxmlparser.HandlePitch
        self.piece = piece.Piece()
        self.data = {"note": None, "direction": None, "expression": None}
        self.data["note"] = note.Note()


class testHandlePitch(pitchin):

    def testNoTags(self):
        self.tags = []
        self.assertEqual(
            None,
            self.handler(
                self.tags,
                self.attrs,
                self.chars,
                self.piece,
                self.data))

    def testIrrelevantTag(self):
        self.tags.append("hello")
        self.assertEqual(
            None,
            self.handler(
                self.tags,
                self.attrs,
                self.chars,
                self.piece,
                self.data))

    def testPitchTag(self):
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)
        self.assertTrue(
            hasattr(
                self.data["note"],
                "pitch"),
            "ERROR: pitch attrib not created")

    def testStepTag(self):
        self.tags.append("step")
        self.chars["step"] = "E"
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)
        self.assertTrue(
            hasattr(
                self.data["note"].pitch,
                "step"),
            "ERRPR: pitch step attrib not set")
        self.assertEqual(
            "E",
            self.data["note"].pitch.step,
            "ERROR: note pitch step value incorrect")

    def testAlterTag(self):
        self.tags.append("alter")
        self.chars["alter"] = "-1"
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)
        self.assertTrue(hasattr(self.data["note"].pitch, "alter"))
        self.assertEqual(-1, self.data["note"].pitch.alter)

    def testOctaveTag(self):
        self.tags.append("octave")
        self.chars["octave"] = "1"
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)
        self.assertTrue(hasattr(self.data["note"].pitch, "octave"))
        self.assertEqual("1", self.data["note"].pitch.octave)


class testUnpitched(pitchin):

    def setUp(self):
        pitchin.setUp(self)
        self.tags.remove("pitch")
        self.tags.append("unpitched")

    def testUnpitchedTag(self):
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)
        self.assertTrue(hasattr(self.data["note"].pitch, "unpitched"))

    def testDisplayStepTag(self):
        self.tags.append("display-step")
        self.chars["display-step"] = "E"
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)
        self.assertTrue(hasattr(self.data["note"].pitch, "step"))

    def testDisplayOctaveTag(self):
        self.tags.append("display-octave")
        self.chars["display-octave"] = "2"
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)
        self.assertTrue(hasattr(self.data["note"].pitch, "octave"))


class testNotehead(testCreateNoteHandler):

    def setUp(self):
        testCreateNoteHandler.setUp(self)
        self.tags.append("notehead")

    def testNoteheadTag(self):
        self.tags = ["note"]
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)
        self.tags = ["note", "notehead"]
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)
        self.assertTrue(hasattr(self.data["note"], "notehead"))
        self.assertIsInstance(self.data["note"].notehead, note.Notehead)

    def testNoteheadFilled(self):
        self.tags = ["note"]
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)
        self.tags.append("notehead")
        self.attrs["notehead"] = {"filled": "yes"}
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)
        self.assertTrue(hasattr(self.data["note"].notehead, "filled"))
        self.assertTrue(self.data["note"].notehead.filled)

    def testNoteheadType(self):
        self.tags = ["note"]
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)
        self.tags.append("notehead")
        self.chars["notehead"] = "diamond"
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)
        self.assertTrue(hasattr(self.data["note"].notehead, "type"))
        self.assertEqual("diamond", self.data["note"].notehead.type)


class testTuplets(notes):

    def setUp(self):
        notes.setUp(self)
        self.tags.append("time-modification")
        self.data["note"] = note.Note()
        self.handler = mxmlparser.handleTimeMod

    def testMod(self):
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)
        self.assertTrue(hasattr(self.data["note"], "timeMod"))

    def testModVal(self):
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)
        self.assertIsInstance(self.data["note"].timeMod, note.TimeModifier)

    def testModNormal(self):
        self.tags.append("normal-notes")
        self.chars["normal-notes"] = "2"
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)
        self.assertTrue(hasattr(self.data["note"].timeMod, "normal"))
        self.assertEqual(2, self.data["note"].timeMod.normal)

    def testModActual(self):
        self.tags.append("actual-notes")
        self.chars["actual-notes"] = "3"
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)
        self.assertTrue(hasattr(self.data["note"].timeMod, "actual"))
        self.assertEqual(3, self.data["note"].timeMod.actual)

    def testTupletTag(self):
        self.tags.append("notations")
        self.tags.append("tuplet")
        self.attrs["tuplet"] = {"type": "stop"}
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)
        direction = self.data["note"].closing_notation[0]
        self.assertIsInstance(direction, note.Tuplet)
