import os

from museparse.tests.testUsingXML.xmlSet import xmlSet, parsePiece
from museparse.classes.ObjectHierarchy.ItemClasses import Clef
from museparse.classes.ObjectHierarchy.TreeClasses.MeasureNode import MeasureNode
from museparse.classes.ObjectHierarchy.TreeClasses.PartNode import PartNode
from museparse.SampleMusicXML import testcases


partname = "clefs.xml"
directory = testcases.__path__._path[0]
piece = parsePiece(os.path.join(directory, partname))


class testClef(xmlSet):

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
                measure=self.m_num,
                staff=1),
            MeasureNode)


class CTests(xmlSet):

    def setUp(self):
        xmlSet.setUp(self)
        self.p_id = "P1"
        self.sign = ""
        self.line = None
        self.clef_octave_change = None
        self.measure = None

    def testClef(self):
        if self.measure is not None:
            measure = piece.getPart(
                self.p_id).getMeasure(
                measure=self.measure,
                staff=1)
            self.assertIsInstance(measure.GetLastClef(), Clef.Clef)

    def testSign(self):
        if self.measure is not None:
            measure = piece.getPart(
                self.p_id).getMeasure(
                measure=self.measure,
                staff=1)

            self.assertEqual(self.sign, measure.GetLastClef().sign)

    def testLine(self):
        if self.measure is not None:
            measure = piece.getPart(
                self.p_id).getMeasure(
                measure=self.measure,
                staff=1)
            self.assertEqual(self.line, measure.GetLastClef().line)

    def testOctaveChange(self):
        if self.measure is not None and self.clef_octave_change is not 0:
            measure = piece.getPart(
                self.p_id).getMeasure(
                measure=self.measure,
                staff=1)
            self.assertEqual(
                self.clef_octave_change,
                measure.GetLastClef().octave_change)


class testMeasure1(CTests):

    def setUp(self):
        CTests.setUp(self)
        self.measure = 1
        self.sign = "G"
        self.line = 2
        self.clef_octave_change = 0


class testMeasure2(CTests):

    def setUp(self):
        CTests.setUp(self)
        self.measure = 2
        self.sign = "G"
        self.line = 2
        self.clef_octave_change = 1


class testMeasure3(CTests):

    def setUp(self):
        CTests.setUp(self)
        self.measure = 3
        self.sign = "G"
        self.line = 2
        self.clef_octave_change = 2


class testMeasure4(CTests):

    def setUp(self):
        CTests.setUp(self)
        self.measure = 4
        self.sign = "G"
        self.line = 2
        self.clef_octave_change = -1


class testMeasure5(CTests):

    def setUp(self):
        CTests.setUp(self)
        self.measure = 5
        self.sign = "G"
        self.line = 1
        self.clef_octave_change = 0


class testMeasure6(CTests):

    def setUp(self):
        CTests.setUp(self)
        self.measure = 6
        self.sign = "C"
        self.line = 1
        self.clef_octave_change = 0


class testMeasure7(CTests):

    def setUp(self):
        CTests.setUp(self)
        self.measure = 7
        self.sign = "C"
        self.line = 2
        self.clef_octave_change = 0


class testMeasure8(CTests):

    def setUp(self):
        CTests.setUp(self)
        self.measure = 8
        self.sign = "C"
        self.line = 3
        self.clef_octave_change = 0


class testMeasure9(CTests):

    def setUp(self):
        CTests.setUp(self)
        self.measure = 9
        self.sign = "C"
        self.line = 4
        self.clef_octave_change = 0


class testMeasure10(CTests):

    def setUp(self):
        CTests.setUp(self)
        self.measure = 10
        self.sign = "C"
        self.line = 5
        self.clef_octave_change = 0


class testMeasure11(CTests):

    def setUp(self):
        CTests.setUp(self)
        self.measure = 11
        self.sign = "F"
        self.line = 4
        self.clef_octave_change = 0


class testMeasure12(CTests):

    def setUp(self):
        CTests.setUp(self)
        self.measure = 12
        self.sign = "F"
        self.line = 4
        self.clef_octave_change = 1


class testMeasure13(CTests):

    def setUp(self):
        CTests.setUp(self)
        self.measure = 13
        self.sign = "F"
        self.line = 4
        self.clef_octave_change = 2


class testMeasure14(CTests):

    def setUp(self):
        CTests.setUp(self)
        self.measure = 14
        self.sign = "F"
        self.line = 4
        self.clef_octave_change = -1


class testMeasure15(CTests):

    def setUp(self):
        CTests.setUp(self)
        self.measure = 15
        self.sign = "F"
        self.line = 4
        self.clef_octave_change = -2


class testMeasure16(CTests):

    def setUp(self):
        CTests.setUp(self)
        self.measure = 16
        self.sign = "F"
        self.line = 3
        self.clef_octave_change = 0


class testMeasure17(CTests):

    def setUp(self):
        CTests.setUp(self)
        self.measure = 17
        self.sign = "F"
        self.line = 5
        self.clef_octave_change = 0
