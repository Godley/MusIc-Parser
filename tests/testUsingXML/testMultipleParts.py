import os

from museparse.tests.testUsingXML.xmlSet import xmlSet, parsePiece
from museparse.classes.ObjectHierarchy.ItemClasses import Part
from museparse.classes.ObjectHierarchy.TreeClasses.PartNode import PartNode
from museparse.classes.ObjectHierarchy.TreeClasses.MeasureNode import MeasureNode


partname = "multiple_parts.xml"
from museparse.SampleMusicXML import testcases
directory = testcases.__path__._path[0]
piece = parsePiece(os.path.join(directory, partname))


class testPart(xmlSet):

    def setUp(self):
        xmlSet.setUp(self)

    def testPartExists(self):
        if hasattr(self, "p_id"):
            self.assertIsInstance(piece.getPart(self.p_id), PartNode)

    def testPartInstance(self):
        if hasattr(self, "p_id"):
            self.assertIsInstance(
                piece.getPart(
                    self.p_id).GetItem(),
                Part.Part)

    def testPartName(self):
        if hasattr(self, "p_id"):
            self.assertEqual(
                self.p_name, piece.getPart(
                    self.p_id).GetItem().name)

    def testMeasures(self):
        if hasattr(self, "p_id"):
            self.assertIsInstance(
                piece.getPart(
                    self.p_id).getMeasure(
                    self.m_num,
                    1),
                MeasureNode)


class testPart1(testPart):

    def setUp(self):
        self.p_id = "P1"
        self.p_name = "Piccolo"
        self.m_num = 32
        testPart.setUp(self)


class testPart2(testPart):

    def setUp(self):
        self.p_id = "P2"
        self.p_name = "Alto Flute"
        self.m_num = 32
        testPart.setUp(self)


class testPart3(testPart):

    def setUp(self):
        self.p_id = "P3"
        self.p_name = "Soprano Recorder"
        self.m_num = 32
        testPart.setUp(self)


class testPart4(testPart):

    def setUp(self):
        self.p_id = "P4"
        self.p_name = "Garklein Recorder"
        self.m_num = 32
        testPart.setUp(self)


class testPart5(testPart):

    def setUp(self):
        self.p_id = "P5"
        self.p_name = "Greatbass Recorder"
        self.m_num = 32
        testPart.setUp(self)
