import os

from museparse.tests.testUsingXML.xmlSet import xmlSet, parsePiece
from museparse.classes.ObjectHierarchy.ItemClasses import BarlinesAndMarkers
from museparse.classes.ObjectHierarchy.TreeClasses.PartNode import PartNode
from museparse.classes.ObjectHierarchy.TreeClasses.MeasureNode import MeasureNode


partname = "WhatHappensWhenIDoThis.xml"
from museparse.SampleMusicXML import testcases
directory = testcases.__path__._path[0]
piece = parsePiece(os.path.join(directory, partname))


class testFile(xmlSet):

    def setUp(self):
        xmlSet.setUp(self)
        self.m_num = 32
        self.p_id = "P1"
        self.p_name = "Piccolo"

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


class testMeasure1(xmlSet):

    def setUp(self):
        self.measure_id = 1
        self.left_number = 1
        self.left_type = "start"
        self.right_number = 1
        self.right_type = "discontinue"
        self.right_repeat = "backward-barline"
        self.right_style = "light-heavy"
        self.measure = piece.getPart("P1").getMeasure(
            measure=self.measure_id, staff=1)

    def testHasBarlines(self):
        self.assertTrue(hasattr(self.measure, "barlines"))

    def testHasLeftBarline(self):
        self.assertTrue("left" in self.measure.barlines)

    def testHasLeftEnding(self):
        self.assertTrue(hasattr(self.measure.GetBarline("left"), "ending"))

    def testLeftEndingInstance(self):
        barline = self.measure.GetBarline("left")
        self.assertIsInstance(barline.ending, BarlinesAndMarkers.EndingMark)

    def testLeftNumber(self):
        barline = self.measure.GetBarline("left")
        self.assertEqual(self.left_number, barline.ending.number)

    def testLeftType(self):
        barline = self.measure.GetBarline("left")
        self.assertEqual(self.left_type, barline.ending.type)

    def testHasRightEnding(self):
        self.assertTrue(hasattr(self.measure.GetBarline("right"), "ending"))

    def testRightEndingInstance(self):
        barline = self.measure.GetBarline("right")
        self.assertIsInstance(barline.ending, BarlinesAndMarkers.EndingMark)

    def testRightNumber(self):
        barline = self.measure.GetBarline("right")
        self.assertEqual(self.right_number, barline.ending.number)

    def testRightType(self):
        barline = self.measure.GetBarline("right")
        self.assertEqual(self.right_type, barline.ending.type)

    def testRightStyle(self):
        barline = self.measure.GetBarline("right")
        self.assertEqual(self.right_style, barline.style)
