import os

from museparse.tests.testUsingXML.xmlSet import xmlSet, parsePiece
from museparse.classes.ObjectHierarchy.ItemClasses import Directions
from museparse.classes.ObjectHierarchy.TreeClasses.PartNode import PartNode
from museparse.classes.ObjectHierarchy.TreeClasses.MeasureNode import MeasureNode
from museparse.classes.ObjectHierarchy.TreeClasses.BaseTree import Search
from museparse.classes.ObjectHierarchy.TreeClasses.NoteNode import Placeholder
from museparse.classes.ObjectHierarchy.TreeClasses.NoteNode import NoteNode
from museparse.classes.ObjectHierarchy.TreeClasses.OtherNodes import DirectionNode
from museparse.SampleMusicXML import testcases


partname = "repeatMarks.xml"
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


class testSegno(xmlSet):

    def setUp(self):
        xmlSet.setUp(self)
        self.m_num = 32
        self.p_id = "P1"
        self.p_name = "Flute"
        self.segno = "segno"
        self.measure_id = 2
        self.item_id = 0
        if hasattr(self, "measure_id"):
            self.measure = piece.getPart(
                self.p_id).getMeasure(
                self.measure_id, 1)

        if hasattr(self, "item_id"):
            note = Search(NoteNode, self.measure, 1)
            self.item = Search(DirectionNode, note, 1).GetItem()

    def testHasAttr(self):
        if hasattr(self, "measure"):
            self.assertTrue(hasattr(self.measure, "segno"))

    def testValue(self):
        if hasattr(self, "measure"):
            self.assertEqual(self.segno, self.measure.segno)


class testCoda(xmlSet):

    def setUp(self):
        xmlSet.setUp(self)
        self.m_num = 32
        self.p_id = "P1"
        self.p_name = "Flute"
        self.measure_id = 3
        self.item_id = 0
        self.coda = "coda"
        if hasattr(self, "measure_id"):
            self.measure = piece.getPart(
                self.p_id).getMeasure(
                self.measure_id, 1)

        if hasattr(self, "item_id"):
            note = Search(NoteNode, self.measure, 1)
            self.item = Search(DirectionNode, note, 1).GetItem()

    def testHasAttr(self):
        if hasattr(self, "measure"):
            self.assertTrue(hasattr(self.measure, "coda"))

    def testValue(self):
        if hasattr(self, "measure"):
            self.assertEqual(self.coda, self.measure.coda)


class testFine(xmlSet):

    def setUp(self):
        xmlSet.setUp(self)
        self.m_num = 32
        self.p_id = "P1"
        self.p_name = "Flute"
        self.measure_id = 6
        self.item_id = 1
        self.fine = True
        if hasattr(self, "measure_id"):
            self.measure = piece.getPart(
                self.p_id).getMeasure(
                self.measure_id, 1)

        if hasattr(self, "item_id"):
            note = Search(Placeholder, self.measure, 1)
            self.item = Search(DirectionNode, note, 1).GetItem()

    def testHasAttr(self):
        if hasattr(self, "measure"):
            self.assertTrue(hasattr(self.measure, "fine"))

    def testValue(self):
        if hasattr(self, "measure"):
            self.assertEqual(self.fine, self.measure.fine)

    def testItem(self):
        if hasattr(self, "item"):
            self.assertIsInstance(self.item, Directions.Direction)

    def testItemType(self):
        if hasattr(self, "item"):
            self.assertEqual("Fine", self.item.text)


class testDaCapo(xmlSet):

    def setUp(self):
        xmlSet.setUp(self)
        self.m_num = 32
        self.p_id = "P1"
        self.measure_id = 7
        self.item_id = 1
        self.dacapo = True
        if hasattr(self, "measure_id"):
            self.measure = piece.getPart(
                self.p_id).getMeasure(
                self.measure_id, 1)

        if hasattr(self, "item_id"):
            note = Search(Placeholder, self.measure, 1)
            self.item = Search(DirectionNode, note, 1).GetItem()

    def testHasAttr(self):
        if hasattr(self, "measure"):
            self.assertTrue(hasattr(self.measure, "dacapo"))

    def testValue(self):
        if hasattr(self, "measure"):
            self.assertEqual(self.dacapo, self.measure.dacapo)

    def testItem(self):
        if hasattr(self, "item"):
            self.assertIsInstance(self.item, Directions.Direction)

    def testItemType(self):
        if hasattr(self, "item"):
            self.assertEqual("D.C.", self.item.text)


class testDaCapoAlFine(xmlSet):

    def setUp(self):
        xmlSet.setUp(self)
        self.m_num = 32
        self.p_id = "P1"
        self.measure_id = 8
        self.item_id = 1
        self.dacapo = True
        if hasattr(self, "measure_id"):
            self.measureNode = piece.getPart(
                self.p_id).getMeasure(
                self.measure_id, 1)

        if hasattr(self, "item_id"):
            note = Search(Placeholder, self.measureNode, 1)
            self.item = Search(DirectionNode, note, 1).GetItem()

    def testHasAttr(self):
        if hasattr(self, "measure"):
            self.assertTrue(hasattr(self.measureNode, "dacapo"))

    def testValue(self):
        if hasattr(self, "measure"):
            self.assertEqual(self.dacapo, self.measureNode.dacapo)

    def testItem(self):
        if hasattr(self, "item"):
            self.assertIsInstance(self.item, Directions.Direction)

    def testItemType(self):
        if hasattr(self, "item"):
            self.assertEqual("D.C. al Fine", self.item.text)


class testDaCapoAlCoda(xmlSet):

    def setUp(self):
        xmlSet.setUp(self)
        self.m_num = 32
        self.p_id = "P1"
        self.measure_id = 9
        self.item_id = 1
        self.dacapo = True
        if hasattr(self, "measure_id"):
            self.measureNode = piece.getPart(
                self.p_id).getMeasure(
                self.measure_id, 1)

        if hasattr(self, "item_id"):
            note = Search(Placeholder, self.measureNode, 1)
            self.item = Search(DirectionNode, note, 1).GetItem()

    def testHasAttr(self):
        if hasattr(self, "measure"):
            self.assertTrue(hasattr(self.measureNode, "dacapo"))

    def testValue(self):
        if hasattr(self, "measure"):
            self.assertEqual(self.dacapo, self.measureNode.dacapo)

    def testItem(self):
        if hasattr(self, "item"):
            self.assertIsInstance(self.item, Directions.Direction)

    def testItemType(self):
        if hasattr(self, "item"):
            self.assertEqual("D.C. al Coda", self.item.text)


class testDalSegnoAlCoda(xmlSet):

    def setUp(self):
        xmlSet.setUp(self)
        self.m_num = 32
        self.p_id = "P1"
        self.measure_id = 10
        self.item_id = 1
        self.dalsegno = "segno"
        if hasattr(self, "measure_id"):
            self.measureNode = piece.getPart(
                self.p_id).getMeasure(
                self.measure_id, 1)

        if hasattr(self, "item_id"):
            note = Search(Placeholder, self.measureNode, 1)
            self.item = Search(DirectionNode, note, 1).GetItem()

    def testHasAttr(self):
        if hasattr(self, "measure"):
            self.assertTrue(hasattr(self.measure, "dalsegno"))

    def testValue(self):
        if hasattr(self, "measure"):
            self.assertEqual(self.dalsegno, self.measure.dalsegno)

    def testItem(self):
        if hasattr(self, "item"):
            self.assertIsInstance(self.item, Directions.Direction)

    def testItemType(self):
        if hasattr(self, "item"):
            self.assertEqual("D.S. al Coda", self.item.text)


class testDalSegnoAlFine(xmlSet):

    def setUp(self):
        xmlSet.setUp(self)
        self.m_num = 32
        self.measure_id = 12
        self.item_id = 1
        self.dalsegno = "segno"
        self.p_id = "P1"
        if hasattr(self, "measure_id"):
            self.measureNode = piece.getPart(
                self.p_id).getMeasure(
                self.measure_id, 1)
            self.measure = self.measureNode.GetItem()

        if hasattr(self, "item_id"):
            note = Search(Placeholder, self.measureNode, 1)
            self.item = Search(DirectionNode, note, 1).GetItem()

    def testHasAttr(self):
        if hasattr(self, "measure"):
            self.assertTrue(hasattr(self.measureNode, "dalsegno"))

    def testValue(self):
        if hasattr(self, "measure"):
            self.assertEqual(self.dalsegno, self.measureNode.dalsegno)

    def testItem(self):
        if hasattr(self, "item"):
            self.assertIsInstance(self.item, Directions.Direction)

    def testItemType(self):
        if hasattr(self, "item"):
            self.assertEqual("D.S. al Fine", self.item.text)


class testDalSegno(xmlSet):

    def setUp(self):
        xmlSet.setUp(self)
        self.measure_id = 13
        self.item_id = 1
        self.dalsegno = "segno"
        self.m_num = 32
        self.p_id = "P1"
        if hasattr(self, "measure_id"):
            self.measureNode = piece.getPart(
                self.p_id).getMeasure(
                self.measure_id, 1)
            self.measure = self.measureNode.GetItem()

        if hasattr(self, "item_id"):
            note = Search(Placeholder, self.measureNode, 1)
            self.item = Search(DirectionNode, note, 1).GetItem()

    def testHasAttr(self):
        if hasattr(self, "measure"):
            self.assertTrue(hasattr(self.measureNode, "dalsegno"))

    def testValue(self):
        if hasattr(self, "measure"):
            self.assertEqual(self.dalsegno, self.measureNode.dalsegno)

    def testItem(self):
        if hasattr(self, "item"):
            self.assertIsInstance(self.item, Directions.Direction)

    def testItemType(self):
        if hasattr(self, "item"):
            self.assertEqual("D.S.", self.item.text)


class testToCoda(xmlSet):

    def setUp(self):
        xmlSet.setUp(self)
        self.measure_id = 14
        self.item_id = 1
        self.tocoda = "coda"
        self.m_num = 32
        self.p_id = "P1"
        if hasattr(self, "measure_id"):
            self.measureNode = piece.getPart(
                self.p_id).getMeasure(
                self.measure_id, 1)

        if hasattr(self, "item_id"):
            note = Search(Placeholder, self.measureNode, 1)
            self.item = Search(DirectionNode, note, 1).GetItem()

    def testHasAttr(self):
        if hasattr(self, "measure"):
            self.assertTrue(hasattr(self.measureNode, "tocoda"))

    def testValue(self):
        if hasattr(self, "measure"):
            self.assertEqual(self.tocoda, self.measureNode.tocoda)

    def testItem(self):
        if hasattr(self, "item"):
            self.assertIsInstance(self.item, Directions.Direction)

    def testItemType(self):
        if hasattr(self, "item"):
            self.assertEqual("To Coda", self.item.text)
