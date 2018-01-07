import os

from museparse.tests.testUsingXML.xmlSet import xmlSet, parsePiece
from museparse.classes.ObjectHierarchy.TreeClasses.PartNode import PartNode
from museparse.classes.ObjectHierarchy.TreeClasses.MeasureNode import MeasureNode
from museparse.classes.ObjectHierarchy.TreeClasses.NoteNode import NoteNode
from museparse.classes.ObjectHierarchy.TreeClasses.BaseTree import Search


partname = "duration_and_stem_direction.xml"
from museparse.SampleMusicXML import testcases
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
                measure=self.m_num,
                staff=1),
            MeasureNode)


class testNoteDurations(xmlSet):

    def setUp(self):
        xmlSet.setUp(self)
        self.m_num = 32
        self.p_id = "P1"
        self.p_name = "Flute"

    def testMeasure1Note1(self):
        part = piece.getPart("P1")
        measure = part.getMeasure(1, 1)
        self.assertIsInstance(Search(NoteNode, measure, 1), NoteNode)

    def testMeasure1Note1Duration(self):
        part = piece.getPart("P1")
        measure = part.getMeasure(1, 1)
        item = Search(NoteNode, measure, 1).GetItem()
        self.assertEqual(1, item.duration)

    def testMeasure2Notes(self):
        part = piece.getPart("P1")
        measure = part.getMeasure(2, 1)
        item = Search(NoteNode, measure, 3)
        self.assertIsInstance(item, NoteNode)

    def testMeasure2Note1(self):
        part = piece.getPart("P1")
        measure = part.getMeasure(2, 1)
        item = Search(NoteNode, measure, 1).GetItem()
        self.assertEqual(2, item.duration)

    def testMeasure2Note2(self):
        part = piece.getPart("P1")
        measure = part.getMeasure(2, 1)
        item = Search(NoteNode, measure, 2).GetItem()
        self.assertEqual(4, item.duration)

    def testMeasure2Note3(self):
        part = piece.getPart("P1")
        measure = part.getMeasure(2, 1)
        item = Search(NoteNode, measure, 3).GetItem()
        self.assertEqual(4, item.duration)

    def testMeasure3Notes(self):
        part = piece.getPart("P1")
        measure = part.getMeasure(3, 1)
        item = Search(NoteNode, measure, 7)
        self.assertIsInstance(item, NoteNode)

    def testMeasure3Note1(self):
        part = piece.getPart("P1")
        measure = part.getMeasure(3, 1)
        item = Search(NoteNode, measure, 1).GetItem()
        self.assertEqual(8, item.duration)

    def testMeasure3Note2(self):
        part = piece.getPart("P1")
        measure = part.getMeasure(3, 1)
        item = Search(NoteNode, measure, 2).GetItem()
        self.assertEqual(16, item.duration)

    def testMeasure3Note3(self):
        part = piece.getPart("P1")
        measure = part.getMeasure(3, 1)
        item = Search(NoteNode, measure, 3).GetItem()
        self.assertEqual(32, item.duration)

    def testMeasure3Note4(self):
        part = piece.getPart("P1")
        measure = part.getMeasure(3, 1)
        item = Search(NoteNode, measure, 4).GetItem()
        self.assertEqual(64, item.duration)

    def testMeasure3Note5(self):
        part = piece.getPart("P1")
        measure = part.getMeasure(3, 1)
        item = Search(NoteNode, measure, 5).GetItem()
        self.assertEqual(64, item.duration)

    def testMeasure3Note6(self):
        part = piece.getPart("P1")
        measure = part.getMeasure(3, 1)
        item = Search(NoteNode, measure, 6).GetItem()
        self.assertEqual(4, item.duration)

    def testMeasure3Note7(self):
        part = piece.getPart("P1")
        measure = part.getMeasure(3, 1)
        item = Search(NoteNode, measure, 7).GetItem()
        self.assertEqual(2, item.duration)


class testStems(xmlSet):

    def setUp(self):
        xmlSet.setUp(self)
        self.m_num = 32
        self.p_id = "P1"
        self.p_name = "Flute"

    def testMeasure1(self):
        part = piece.getPart("P1")
        measure = part.getMeasure(1, 1)
        note = Search(NoteNode, measure, 1).GetItem()
        self.assertFalse(hasattr(note, "stem"))

    def testMeasure2Note1(self):
        part = piece.getPart("P1")
        measure = part.getMeasure(2, 1)
        note = Search(NoteNode, measure, 1).GetItem()
        self.assertTrue(hasattr(note, "stem"))

    def testMeasure2Note1Direction(self):
        part = piece.getPart("P1")
        measure = part.getMeasure(2, 1)
        note = Search(NoteNode, measure, 1).GetItem()
        self.assertEqual("up", note.stem.type)

    def testMeasure2Note2(self):
        part = piece.getPart("P1")
        measure = part.getMeasure(2, 1)
        note = Search(NoteNode, measure, 2).GetItem()
        self.assertTrue(hasattr(note, "stem"))

    def testMeasure2Note2Direction(self):
        part = piece.getPart("P1")
        measure = part.getMeasure(2, 1)
        note = Search(NoteNode, measure, 2).GetItem()
        self.assertEqual("up", note.stem.type)

    def testMeasure2Note3(self):
        part = piece.getPart("P1")
        measure = part.getMeasure(2, 1)
        note = Search(NoteNode, measure, 3).GetItem()
        self.assertTrue(hasattr(note, "stem"))

    def testMeasure2Note3Direction(self):
        part = piece.getPart("P1")
        measure = part.getMeasure(2, 1)
        note = Search(NoteNode, measure, 3).GetItem()
        self.assertEqual("up", note.stem.type)

    def testMeasure3Note1(self):
        part = piece.getPart("P1")
        measure = part.getMeasure(3, 1)
        note = Search(NoteNode, measure, 1).GetItem()
        self.assertTrue(hasattr(note, "stem"))

    def testMeasure3Note1Direction(self):
        part = piece.getPart("P1")
        measure = part.getMeasure(3, 1)
        note = Search(NoteNode, measure, 1).GetItem()
        self.assertEqual("down", note.stem.type)

    def testMeasure3Note2(self):
        part = piece.getPart("P1")
        measure = part.getMeasure(3, 1)
        note = Search(NoteNode, measure, 2).GetItem()
        self.assertTrue(hasattr(note, "stem"))

    def testMeasure3Note2Direction(self):
        part = piece.getPart("P1")
        measure = part.getMeasure(3, 1)
        note = Search(NoteNode, measure, 2).GetItem()
        self.assertEqual("down", note.stem.type)

    def testMeasure3Note3(self):
        part = piece.getPart("P1")
        measure = part.getMeasure(3, 1)
        note = Search(NoteNode, measure, 3).GetItem()
        self.assertTrue(hasattr(note, "stem"))

    def testMeasure3Note3Direction(self):
        part = piece.getPart("P1")
        measure = part.getMeasure(3, 1)
        note = Search(NoteNode, measure, 3).GetItem()
        self.assertEqual("down", note.stem.type)

    def testMeasure3Note4(self):
        part = piece.getPart("P1")
        measure = part.getMeasure(3, 1)
        note = Search(NoteNode, measure, 4).GetItem()
        self.assertTrue(hasattr(note, "stem"))

    def testMeasure3Note4Direction(self):
        part = piece.getPart("P1")
        measure = part.getMeasure(3, 1)
        note = Search(NoteNode, measure, 4).GetItem()
        self.assertEqual("down", note.stem.type)
