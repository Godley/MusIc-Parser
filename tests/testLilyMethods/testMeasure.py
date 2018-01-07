import unittest

from museparse.classes.ObjectHierarchy.ItemClasses import Directions, BarlinesAndMarkers, Meter, Note
from museparse.tests.testLilyMethods.lily import Lily
from museparse.classes.ObjectHierarchy.TreeClasses.NoteNode import NoteNode
from museparse.classes.ObjectHierarchy.TreeClasses.MeasureNode import MeasureNode
from museparse.classes.ObjectHierarchy.TreeClasses.StaffNode import StaffNode


class MeasureTests(Lily):

    def testValue(self):
        if hasattr(self, "lilystring"):
            if hasattr(self, "item"):
                self.assertEqual(self.lilystring, self.item.to_lily())


class testMeasure(MeasureTests):

    def setUp(self):
        self.item = MeasureNode()
        self.lilystring = " | "


class testMeasureNote(MeasureTests):

    def setUp(self):
        self.item = MeasureNode()
        note = Note.Note()
        note.pitch = Note.Pitch()
        self.item.addNote(note)
        self.lilystring = "c'  | "
        self.compile = True
        self.wrappers = ["\\new Staff {", "}"]
        Lily.setUp(self)
        self.name = "measurenote"


class testMeasureChord(MeasureTests):

    def setUp(self):
        self.item = MeasureNode()
        note = Note.Note()
        note.pitch = Note.Pitch()
        self.item.addNote(note)
        note2 = Note.Note(chord=True)
        note2.pitch = Note.Pitch()
        self.item.addNote(note2, chord=True)
        self.lilystring = "<c' c'>  | "
        self.compile = True
        self.wrappers = ["\\new Staff {", "}"]
        Lily.setUp(self)
        self.name = "measurenotechord"


class testMeasureNoteWithGrace(MeasureTests):

    def setUp(self):
        self.item = MeasureNode()
        note = Note.Note(type="quarter")
        note.pitch = Note.Pitch()
        grace = Note.GraceNote(first=True)
        grace.last = True
        note.add_notation(grace)
        self.item.addNote(note)
        self.item.RunVoiceChecks()
        self.lilystring = "\grace { c'4 }  | "
        self.compile = True
        self.wrappers = ["\\new Staff {", "}"]
        Lily.setUp(self)
        self.name = "measurenotegrace"


class testMeasureTempo(MeasureTests):

    def setUp(self):
        self.item = MeasureNode()
        self.item.addDirection(Directions.Metronome(beat="quarter", min=60))
        self.item.addNote(NoteNode())
        self.lilystring = " \\tempo 4=60  | "
        self.compile = True
        self.wrappers = ["\\new Staff {", "}"]
        Lily.setUp(self)
        self.name = "measuretempo"


class testMeasureTwoDirections(MeasureTests):

    def setUp(self):
        self.item = MeasureNode()
        self.item.addDirection(
            Directions.Direction(
                text="hello world",
                placement="above"))
        self.item.addDirection(Directions.Metronome(beat="quarter", min=60))
        self.item.addNote(NoteNode())
        self.lilystring = " ^\\markup { \"hello world\"  } \\tempo 4=60  | "
        self.compile = True
        self.wrappers = ["\\new Staff {", "}"]
        Lily.setUp(self)
        self.name = "measuretwodirections"


class testMeasureTwoNotes(MeasureTests):

    def setUp(self):
        self.item = MeasureNode()
        note = Note.Note()
        note.pitch = Note.Pitch()
        self.item.addNote(note)
        note2 = Note.Note()
        note2.pitch = Note.Pitch()
        self.item.addNote(note2)
        self.lilystring = "c' c'  | "
        self.compile = True
        self.wrappers = ["\\new Staff {", "}"]
        Lily.setUp(self)
        self.name = "measuretwonotes"


class testMeasureOneNoteOneDirection(MeasureTests):

    def setUp(self):
        self.item = MeasureNode()
        note = Note.Note()
        note.pitch = Note.Pitch()
        self.item.addDirection(
            Directions.Direction(
                text="hello",
                placement="below"))
        self.item.addNote(note)
        self.lilystring = "c' _\\markup { \"hello\"  }  | "
        self.compile = True
        self.wrappers = ["\\new Staff {", "}"]
        Lily.setUp(self)
        self.name = "measurenotedirection"


class testPartialMeasure(MeasureTests):

    def setUp(self):
        self.item = MeasureNode()
        self.item.partial = True
        self.item.meter = Meter.Meter(beats=4, type=4)
        note = Note.Note(type="quarter")
        note.pitch = Note.Pitch()
        self.item.addNote(note)
        self.lilystring = "\\time 4/4 \partial 4 c'4  | "
        self.compile = True
        self.wrappers = ["\\new Staff {", "}"]
        Lily.setUp(self)
        self.name = "measurePartial"


class testPartialMeasureTwoNotes(Lily):

    def setUp(self):
        self.item = MeasureNode(partial=True)
        self.item.meter = Meter.Meter(type=4, beats=4)
        note = Note.Note()
        note.set_type("quarter")
        note.pitch = Note.Pitch(octave=4)
        note2 = Note.Note()
        note2.set_type("quarter")
        note2.pitch = Note.Pitch(octave=4)
        self.item.addNote(note)
        self.item.addNote(note2)
        Lily.setUp(self)
        self.lilystring = "\\time 4/4 \partial 2 c'4 c'4  | "


class testPartialMeasureTwoNotesDifferentTypes(Lily):

    def setUp(self):
        self.item = MeasureNode(partial=True)
        self.item.meter = Meter.Meter(type=4, beats=4)
        note = Note.Note()
        note.set_type("quarter")
        note.pitch = Note.Pitch(octave=4)
        note2 = Note.Note()
        note2.set_type("half")
        note2.pitch = Note.Pitch(octave=4)
        self.item.addNote(note)
        self.item.addNote(note2)
        Lily.setUp(self)
        self.lilystring = "\\time 4/4 \partial 2. c'4 c'2  | "


class testPartialMeasureThreeNotesDifferentTypes(Lily):

    def setUp(self):
        self.item = MeasureNode(partial=True)
        self.item.meter = Meter.Meter(type=4, beats=4)
        note = Note.Note(type="quarter")
        note.pitch = Note.Pitch(octave=4)
        note2 = Note.Note(type="half")
        note2.pitch = Note.Pitch(octave=4)
        note3 = Note.Note(type="eighth")
        note3.pitch = Note.Pitch(octave=4)
        self.item.addNote(note)
        self.item.addNote(note2)
        self.item.addNote(note3)
        Lily.setUp(self)
        self.lilystring = "\\time 4/4 \partial 2.. c'4 c'2 c'8  | "


class testPartialMeasureThreeNotesSameTypes(Lily):

    def setUp(self):
        self.item = MeasureNode(partial=True)
        self.item.meter = Meter.Meter(type=4, beats=4)
        note = Note.Note(type="quarter")
        note.pitch = Note.Pitch(octave=4)
        note2 = Note.Note(type="quarter")
        note2.pitch = Note.Pitch(octave=4)
        note3 = Note.Note(type="quarter")
        note3.pitch = Note.Pitch(octave=4)
        self.item.addNote(note)
        self.item.addNote(note2)
        self.item.addNote(note3)
        Lily.setUp(self)
        self.lilystring = "\\time 4/4 \partial 2. c'4 c'4 c'4  | "


class testMeasureOrder(Lily):

    def setUp(self):
        self.item = StaffNode()
        measure1 = MeasureNode()
        self.item.AddChild(measure1, index=1)
        measure2 = MeasureNode()
        measure3 = MeasureNode()
        self.item.AddChild(measure2, index="X1")
        self.item.AddChild(measure3, index=2)
        self.lilystring = " % measure 1\n | \n\n % measure X1\n | \n\n % measure 2\n | \n\n"


class testMeasureTranspositionCalc(unittest.TestCase):

    def setUp(self):
        self.item = MeasureNode()

    def testCalcUpWithChromatic(self):
        self.item.transpose = BarlinesAndMarkers.Transposition(chromatic=2)
        expected = "\\transpose c' d' {"
        self.assertEqual(self.item.CalculateTransposition(), expected)

    def testCalcUpWithDiatonic(self):
        self.item.transpose = BarlinesAndMarkers.Transposition(diatonic=1)
        expected = "\\transpose c' d' {"
        self.assertEqual(self.item.CalculateTransposition(), expected)

    def testCalcOctaveShift(self):
        self.item.transpose = BarlinesAndMarkers.Transposition(octave=1)
        expected = "\\transpose c' c'' {"
        self.assertEqual(self.item.CalculateTransposition(), expected)


class testMeasureNoteWithShifter(Lily):

    def setUp(self):
        self.item = MeasureNode()
        node = NoteNode()
        node.GetItem().pitch = Note.Pitch(octave=4)
        self.item.addNote(node)
        dirnode = Directions.OctaveShift(amount=8, type="up")
        self.item.addDirection(dirnode)
        node2 = NoteNode()
        node2.GetItem().pitch = Note.Pitch(octave=4)
        self.item.addNote(node2)
        Lily.setUp(self)
        self.compile = True
        self.wrappers = ["\\new Staff{a8 ", "c'8]}"]
        self.lilystring = "c' \n\\ottava #-1\n c'  | "
        self.name = "noteOctaveShift"


class testShiftBeforeNote(unittest.TestCase):

    def setUp(self):
        self.item = MeasureNode()
        dirnode = Directions.OctaveShift(amount=8, type="up")
        self.item.addDirection(dirnode)
        self.node = NoteNode()
        self.node.GetItem().pitch = Note.Pitch(octave=2)
        self.item.addNote(self.node)

    def testLilystring(self):
        value = "\n\\ottava #-1\n c,  | "
        self.assertEqual(value, self.item.to_lily())


class testGraceAtStartOfMeasure(unittest.TestCase):

    def setUp(self):
        self.item = MeasureNode()
        node = NoteNode()
        self.note = Note.Note(type="quarter")
        self.note.add_notation(Note.GraceNote())
        self.note.pitch = Note.Pitch()
        node.SetItem(self.note)
        self.item.addNote(node)
        self.item.RunVoiceChecks()

    def testIsFirstGraceNote(self):
        result = self.note.search(Note.GraceNote)
        self.assertTrue(result.first)

    def testLilystring(self):
        value = "\grace { c'4 }  | "
        self.assertEqual(value, self.item.to_lily())


class testTwoVoicesMeasureNotePosition(Lily):

    def setUp(self):
        self.item = MeasureNode()
        node = Note.Note(type="quarter")
        node.pitch = Note.Pitch(octave=4)
        self.item.addNote(node, voice=1)
        self.item.addNote(node, voice=1)
        self.item.Backup(1)
        node2 = Note.Note(type="quarter")
        node2.pitch = Note.Pitch(octave=4)
        self.item.addNote(node2, voice=2)
        Lily.setUp(self)
        self.compile = True
        self.wrappers = ["\\new Staff{a8 ", "c'8]}"]
        self.lilystring = "<< % voice 1\n\\new Voice = \"one\"\n{\\voiceOne c'4 c'4 } % voice 2\n\\new Voice = \"two\"\n{\\voiceTwo r4 c'4 }>> | "
        self.name = "noteOctaveShift"

    def tearDown(self):
        self.item = None
