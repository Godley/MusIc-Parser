import os

from museparse.tests.testUsingXML.xmlSet import xmlSet, parsePiece
from museparse.classes.ObjectHierarchy.ItemClasses import Ornaments
from museparse.classes.ObjectHierarchy.TreeClasses.PartNode import PartNode
from museparse.classes.ObjectHierarchy.TreeClasses.MeasureNode import MeasureNode
from museparse.classes.ObjectHierarchy.TreeClasses.BaseTree import Search
from museparse.classes.ObjectHierarchy.TreeClasses.NoteNode import NoteNode
from museparse.SampleMusicXML import testcases


partname = "Tremolo.xml"
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


class testTremolo(xmlSet):

    def setUp(self):
        self.p_id = "P1"
        if hasattr(self, "measure_id"):
            self.measure = piece.getPart(
                self.p_id).getMeasure(
                self.measure_id, 1)
        if hasattr(self, "item_id"):
            self.item = Search(
                NoteNode,
                self.measure,
                self.item_id +
                1).GetItem()
        if hasattr(self, "notation_id"):
            if self.type == "stop":
                self.notation = self.item.closing_notation[self.notation_id]
            else:
                self.notation = self.item.prenotation[self.notation_id]

    def testHasNotations(self):
        if hasattr(self, "item"):
            if not hasattr(self, "notate_num"):
                if self.type == "stop":
                    self.assertEqual(1, len(self.item.wrap_notation))
                else:
                    self.assertEqual(1, len(self.item.prenotation))
            else:
                if self.type == "stop":
                    self.assertEqual(
                        self.notate_num, len(
                            self.item.closing_notation))
                else:
                    self.assertEqual(
                        self.notate_num, len(
                            self.item.prenotation))

    def testNotationInstance(self):
        if hasattr(self, "notation"):
            self.assertIsInstance(self.notation, Ornaments.Tremolo)

    def testTremoloType(self):
        if hasattr(self, "notation"):
            self.assertEqual(self.type, self.notation.type)

    def testTremoloValue(self):
        if hasattr(self, "notation"):
            self.assertEqual(self.value, self.notation.value)


class testMeasure1Note1(testTremolo):

    def setUp(self):
        self.measure_id = 1
        self.item_id = 0
        self.notation_id = 0
        self.type = "single"
        self.value = 1
        testTremolo.setUp(self)


class testMeasure1Note2(testTremolo):

    def setUp(self):
        self.measure_id = 1
        self.item_id = 1
        self.notation_id = 0
        self.type = "single"
        self.value = 2
        testTremolo.setUp(self)


class testMeasure1Note3(testTremolo):

    def setUp(self):
        self.measure_id = 1
        self.item_id = 2
        self.notation_id = 0
        self.type = "single"
        self.value = 3
        testTremolo.setUp(self)


class testMeasure2Note1(testTremolo):

    def setUp(self):
        self.measure_id = 2
        self.item_id = 0
        self.notation_id = 0
        self.type = "start"
        self.value = 2
        testTremolo.setUp(self)


class testMeasure2Note2Notation0(testTremolo):

    def setUp(self):
        self.measure_id = 2
        self.item_id = 1
        self.notation_id = 0
        self.type = "stop"
        self.value = 2
        self.notate_num = 1
        testTremolo.setUp(self)
