import os

from museparse.tests.testUsingXML.xmlSet import xmlSet, parsePiece
from museparse.classes.ObjectHierarchy.ItemClasses import BarlinesAndMarkers
from museparse.classes.ObjectHierarchy.TreeClasses.MeasureNode import MeasureNode
from museparse.SampleMusicXML import testcases


partname = "barlines.xml"
directory = testcases.__path__._path[0]
piece = parsePiece(os.path.join(directory, partname))


class testBarlines(xmlSet):

    def setUp(self):
        xmlSet.setUp(self)
        self.m_num = 32
        self.p_id = "P1"
        self.p_name = "Piano"

    def testParts(self):
        global piece
        self.assertTrue(self.p_id in piece.root.GetChildrenIndexes())
        self.assertEqual(self.p_name, piece.getPart(self.p_id).GetItem().name)

    def testMeasures(self):
        self.assertIsInstance(
            piece.getPart(
                self.p_id).getMeasure(
                measure=1,
                staff=1),
            MeasureNode)

    def testMeasure2Barline(self):
        part = piece.getPart(self.p_id)
        item = part.getMeasure(measure=2, staff=1)
        self.assertTrue(hasattr(item, "barlines"))

    def testMeasure2BarlineLocation(self):
        part = piece.getPart(self.p_id)
        item = part.getMeasure(measure=2, staff=1)
        self.assertTrue("right" in item.barlines)

    def testMeasure2BarlineInstance(self):
        part = piece.getPart(self.p_id)
        item = part.getMeasure(measure=2, staff=1)
        self.assertIsInstance(
            item.barlines["right"],
            BarlinesAndMarkers.Barline)

    def testMeasure2BarlineStyle(self):
        part = piece.getPart(self.p_id)
        item = part.getMeasure(measure=2, staff=1)
        self.assertEqual("dashed", item.barlines["right"].style)

    def testMeasure4Barline(self):
        part = piece.getPart(self.p_id)
        item = part.getMeasure(measure=4, staff=1)
        self.assertTrue(hasattr(item, "barlines"))

    def testMeasure4BarlineInstance(self):
        part = piece.getPart(self.p_id)
        item = part.getMeasure(measure=4, staff=1)
        self.assertIsInstance(
            item.barlines["right"],
            BarlinesAndMarkers.Barline)

    def testMeasure4BarlineRight(self):
        part = piece.getPart(self.p_id)
        item = part.getMeasure(measure=4, staff=1)
        self.assertTrue("right" in item.barlines)

    def testMeasure4BarlineRightStyle(self):
        part = piece.getPart(self.p_id)
        item = part.getMeasure(measure=4, staff=1)
        self.assertEqual("light-heavy", item.barlines["right"].style)

    def testMeasure5Barline(self):
        part = piece.getPart(self.p_id)
        item = part.getMeasure(measure=5, staff=1)
        self.assertTrue(hasattr(item, "barlines"))

    def testMeasure5BarlineRight(self):
        part = piece.getPart(self.p_id)
        item = part.getMeasure(measure=5, staff=1)
        self.assertTrue("right" in item.barlines)

    def testMeasure5BarlineRightInstance(self):
        part = piece.getPart(self.p_id)
        item = part.getMeasure(measure=5, staff=1)
        self.assertIsInstance(
            item.barlines["right"],
            BarlinesAndMarkers.Barline)

    def testMeasure5BarlineStyle(self):
        part = piece.getPart(self.p_id)
        item = part.getMeasure(measure=5, staff=1)
        self.assertEqual("light-light", item.barlines["right"].style)
