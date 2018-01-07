import os

from museparse.tests.testUsingXML.xmlSet import xmlSet, parsePiece
from museparse.classes.ObjectHierarchy.ItemClasses import Mark
from museparse.classes.ObjectHierarchy.TreeClasses.PartNode import PartNode
from museparse.classes.ObjectHierarchy.TreeClasses.BaseTree import Search
from museparse.classes.ObjectHierarchy.TreeClasses.MeasureNode import MeasureNode
from museparse.classes.ObjectHierarchy.TreeClasses.NoteNode import NoteNode
from museparse.SampleMusicXML import testcases


partname = "fingering.xml"
directory = testcases.__path__._path[0]
piece = parsePiece(os.path.join(directory, partname))


class testFile(xmlSet):

    def setUp(self):
        xmlSet.setUp(self)
        self.m_num = 32
        self.p_id = "P1"
        self.p_name = "Flute"

    def testParts(self):
        global piece
        self.assertIsInstance(piece.getPart(self.p_id), PartNode)
        self.assertEqual(self.p_name, piece.getPart(self.p_id).GetItem().name)

    def testMeasures(self):
        self.assertIsInstance(
            piece.getPart(
                self.p_id).getMeasure(
                self.m_num,
                1),
            MeasureNode)


class testFingering(xmlSet):

    def setUp(self):
        xmlSet.setUp(self)
        self.m_num = 32
        self.p_id = "P1"
        self.p_name = "Flute"
        if hasattr(self, "measure_id"):
            self.measure = piece.getPart(
                self.p_id).getMeasure(
                self.measure_id, 1)

    def testMeasureNoteInstance(self):
        if hasattr(self, "note_id"):
            note = Search(NoteNode, self.measure, self.note_id + 1)
            self.assertIsInstance(
                note.GetItem().postnotation[0],
                Mark.Technique)

    def testMeasureNoteType(self):
        if hasattr(self, "note_id") and hasattr(self, "type"):
            note = Search(NoteNode, self.measure, self.note_id + 1)
            self.assertEqual(self.type, note.GetItem().postnotation[0].type)

    def testMeasureNoteSymbol(self):
        if hasattr(self, "note_id") and hasattr(self, "symbol"):
            note = Search(NoteNode, self.measure, self.note_id + 1)
            self.assertEqual(self.symbol,
                             note.GetItem().postnotation[0].symbol)


class testMeasure1Note1(testFingering):

    def setUp(self):
        self.p_id = "P1"
        self.measure_id = 1
        self.note_id = 0
        self.type = "fingering"
        self.symbol = "0"
        testFingering.setUp(self)


class testMeasure1Note2(testFingering):

    def setUp(self):
        self.p_id = "P1"
        self.measure_id = 1
        self.note_id = 1
        self.type = "fingering"
        self.symbol = "1"
        testFingering.setUp(self)


class testMeasure1Note3(testFingering):

    def setUp(self):
        self.p_id = "P1"
        self.measure_id = 1
        self.note_id = 2
        self.type = "fingering"
        self.symbol = "2"
        testFingering.setUp(self)


class testMeasure1Note4(testFingering):

    def setUp(self):
        self.p_id = "P1"
        self.measure_id = 1
        self.note_id = 3
        self.type = "fingering"
        self.symbol = "4"
        testFingering.setUp(self)


class testMeasure2Note1(testFingering):

    def setUp(self):
        self.p_id = "P1"
        self.measure_id = 2
        self.note_id = 0
        self.type = "fingering"
        self.symbol = "5"
        testFingering.setUp(self)


class testMeasure2Note2(testFingering):

    def setUp(self):
        self.p_id = "P1"
        self.measure_id = 2
        self.note_id = 1
        self.type = "pluck"
        self.symbol = "p"
        testFingering.setUp(self)


class testMeasure2Note3(testFingering):

    def setUp(self):
        self.p_id = "P1"
        self.measure_id = 2
        self.note_id = 2
        self.type = "pluck"
        self.symbol = "i"
        testFingering.setUp(self)


class testMeasure2Note4(testFingering):

    def setUp(self):
        self.p_id = "P1"
        self.measure_id = 2
        self.note_id = 3
        self.type = "pluck"
        self.symbol = "m"
        testFingering.setUp(self)


class testMeasure3Note1(testFingering):

    def setUp(self):
        self.p_id = "P1"
        self.measure_id = 3
        self.note_id = 0
        self.type = "pluck"
        self.symbol = "a"
        testFingering.setUp(self)


class testMeasure3Note2(testFingering):

    def setUp(self):
        self.p_id = "P1"
        self.measure_id = 3
        self.note_id = 1
        self.type = "pluck"
        self.symbol = "c"
        testFingering.setUp(self)


class testMeasure3Note3(testFingering):

    def setUp(self):
        self.p_id = "P1"
        self.measure_id = 3
        self.note_id = 2
        self.type = "string"
        self.symbol = "0"
        testFingering.setUp(self)


class testMeasure3Note4(testFingering):

    def setUp(self):
        self.p_id = "P1"
        self.measure_id = 3
        self.note_id = 3
        self.type = "string"
        self.symbol = "1"
        testFingering.setUp(self)


class testMeasure4Note1(testFingering):

    def setUp(self):
        self.p_id = "P1"
        self.measure_id = 4
        self.note_id = 0
        self.type = "string"
        self.symbol = "2"
        testFingering.setUp(self)


class testMeasure4Note2(testFingering):

    def setUp(self):
        self.p_id = "P1"
        self.measure_id = 4
        self.note_id = 1
        self.type = "string"
        self.symbol = "3"
        testFingering.setUp(self)


class testMeasure4Note3(testFingering):

    def setUp(self):
        self.p_id = "P1"
        self.measure_id = 4
        self.note_id = 2
        self.type = "string"
        self.symbol = "4"
        testFingering.setUp(self)


class testMeasure4Note4(testFingering):

    def setUp(self):
        self.p_id = "P1"
        self.measure_id = 4
        self.note_id = 3
        self.type = "string"
        self.symbol = "5"
        testFingering.setUp(self)


class testMeasure5Note1(testFingering):

    def setUp(self):
        self.p_id = "P1"
        self.measure_id = 5
        self.note_id = 0
        self.type = "string"
        self.symbol = "6"
        testFingering.setUp(self)
