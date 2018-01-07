import os

from museparse.tests.testUsingXML.xmlSet import xmlSet, parsePiece
from museparse.classes.ObjectHierarchy.ItemClasses import Note
from museparse.classes.ObjectHierarchy.TreeClasses.PartNode import PartNode
from museparse.classes.ObjectHierarchy.TreeClasses.MeasureNode import MeasureNode
from museparse.classes.ObjectHierarchy.TreeClasses.BaseTree import Search
from museparse.classes.ObjectHierarchy.TreeClasses.NoteNode import NoteNode


partname = "tuplets.xml"
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

    def testmeasures(self):
        self.assertIsInstance(
            piece.getPart(
                self.p_id).getMeasure(
                self.m_num,
                1),
            MeasureNode)


class testTimeMod(xmlSet):

    def setUp(self):
        xmlSet.setUp(self)
        if hasattr(self, "measure_id"):
            self.measure = piece.getPart("P1").getMeasure(self.measure_id, 1)

        if hasattr(self, "item_id"):
            self.item = Search(
                NoteNode,
                self.measure,
                self.item_id +
                1).GetItem()

    def testHasTimeMod(self):
        if hasattr(self, "item"):
            self.assertTrue(hasattr(self.item, "timeMod"))

    def testInstance(self):
        if hasattr(self, "item"):
            self.assertIsInstance(self.item.timeMod, Note.TimeModifier)

    def testActual(self):
        if hasattr(self, "item"):
            self.assertEqual(self.actual, self.item.timeMod.actual)

    def testNormal(self):
        if hasattr(self, "item"):
            self.assertEqual(self.normal, self.item.timeMod.normal)

    def testInstanceTuplet(self):
        if hasattr(self, "notation_id"):
            if hasattr(self, "type") and self.type == "start":
                self.assertIsInstance(
                    self.item.prenotation[
                        self.notation_id], Note.Tuplet)
            else:
                self.assertIsInstance(
                    self.item.closing_notation[
                        self.notation_id], Note.Tuplet)

    def testType(self):
        if hasattr(self, "item") and hasattr(self, "type"):
            if self.type == "start":
                self.assertEqual(
                    self.type, self.item.prenotation[
                        self.notation_id].type)

            else:
                self.assertEqual(
                    self.type, self.item.closing_notation[
                        self.notation_id].type)

    def testBracket(self):
        if hasattr(self, "item") and hasattr(self, "bracket"):
            if self.type == "start":
                self.assertEqual(
                    self.bracket, self.item.prenotation[
                        self.notation_id].bracket)

            else:
                self.assertEqual(
                    self.bracket, self.item.postnotation[
                        self.notation_id].bracket)


class testMeasure1Note1(testTimeMod):

    def setUp(self):
        self.actual = 2
        self.normal = 2
        self.type = "start"
        self.bracket = True
        self.measure_id = 1
        self.item_id = 0
        self.notation_id = 0
        testTimeMod.setUp(self)


class testMeasure1note2(testTimeMod):

    def setUp(self):
        self.actual = 2
        self.normal = 2
        self.type = "stop"
        self.measure_id = 1
        self.item_id = 1
        self.notation_id = 0
        testTimeMod.setUp(self)


class testMeasure2Note1(testTimeMod):

    def setUp(self):
        self.actual = 3
        self.normal = 2
        self.type = "start"
        self.bracket = True
        self.measure_id = 2
        self.item_id = 0
        self.notation_id = 0
        testTimeMod.setUp(self)


class testMeasure2note2(testTimeMod):

    def setUp(self):
        self.actual = 3
        self.normal = 2
        self.measure_id = 2
        self.item_id = 1
        testTimeMod.setUp(self)


class testMeasure2Note3(testTimeMod):

    def setUp(self):
        self.actual = 3
        self.normal = 2
        self.type = "stop"
        self.measure_id = 2
        self.item_id = 2
        self.notation_id = 0
        testTimeMod.setUp(self)


class testMeasure2Note4(testTimeMod):

    def setUp(self):
        self.actual = 4
        self.normal = 4
        self.type = "start"
        self.bracket = False
        self.measure_id = 2
        self.item_id = 3
        self.notation_id = 0
        testTimeMod.setUp(self)


class testMeasure2Note5(testTimeMod):

    def setUp(self):
        self.actual = 4
        self.normal = 4
        self.measure_id = 2
        self.item_id = 4
        testTimeMod.setUp(self)


class testMeasure2Note6(testTimeMod):

    def setUp(self):
        self.actual = 4
        self.normal = 4
        self.measure_id = 2
        self.item_id = 5
        testTimeMod.setUp(self)


class testMeasure2Note7(testTimeMod):

    def setUp(self):
        self.actual = 4
        self.normal = 4
        self.measure_id = 2
        self.item_id = 6
        self.notation_id = 0
        self.type = "stop"
        testTimeMod.setUp(self)


class testMeasure2Note8(testTimeMod):

    def setUp(self):
        self.actual = 5
        self.normal = 4
        self.measure_id = 2
        self.item_id = 7
        self.notation_id = 0
        self.type = "start"
        self.bracket = False
        testTimeMod.setUp(self)


class testMeasure2Note9(testTimeMod):

    def setUp(self):
        self.actual = 5
        self.normal = 4
        self.measure_id = 2
        self.item_id = 8
        testTimeMod.setUp(self)


class testMeasure2Note10(testTimeMod):

    def setUp(self):
        self.actual = 5
        self.normal = 4
        self.measure_id = 2
        self.item_id = 9
        testTimeMod.setUp(self)


class testMeasure2Note11(testTimeMod):

    def setUp(self):
        self.actual = 5
        self.normal = 4
        self.measure_id = 2
        self.item_id = 10
        testTimeMod.setUp(self)


class testMeasure2Note12(testTimeMod):

    def setUp(self):
        self.actual = 5
        self.normal = 4
        self.measure_id = 2
        self.item_id = 11
        self.notation_id = 0
        self.type = "stop"
        testTimeMod.setUp(self)


class testMeasure3Note1(testTimeMod):

    def setUp(self):
        self.actual = 6
        self.normal = 4
        self.measure_id = 3
        self.item_id = 0
        self.notation_id = 0
        self.type = "start"
        self.bracket = True
        testTimeMod.setUp(self)


class testMeasure3Note2(testTimeMod):

    def setUp(self):
        self.actual = 6
        self.normal = 4
        self.measure_id = 3
        self.item_id = 1
        testTimeMod.setUp(self)


class testMeasure3Note3(testTimeMod):

    def setUp(self):
        self.actual = 6
        self.normal = 4
        self.measure_id = 3
        self.item_id = 2
        testTimeMod.setUp(self)


class testMeasure3Note4(testTimeMod):

    def setUp(self):
        self.actual = 6
        self.normal = 4
        self.measure_id = 3
        self.item_id = 3
        testTimeMod.setUp(self)


class testMeasure3Note5(testTimeMod):

    def setUp(self):
        self.actual = 6
        self.normal = 4
        self.measure_id = 3
        self.item_id = 4
        testTimeMod.setUp(self)


class testMeasure3Note6(testTimeMod):

    def setUp(self):
        self.actual = 6
        self.normal = 4
        self.measure_id = 3
        self.item_id = 5
        self.notation_id = 0
        self.type = "stop"
        testTimeMod.setUp(self)


class testMeasure4Note1(testTimeMod):

    def setUp(self):
        self.actual = 7
        self.normal = 4
        self.measure_id = 4
        self.item_id = 0
        self.notation_id = 0
        self.type = "start"
        self.bracket = True
        testTimeMod.setUp(self)


class testMeasure4Note2(testTimeMod):

    def setUp(self):
        self.actual = 7
        self.normal = 4
        self.measure_id = 4
        self.item_id = 1
        testTimeMod.setUp(self)


class testMeasure4Note3(testTimeMod):

    def setUp(self):
        self.actual = 7
        self.normal = 4
        self.measure_id = 4
        self.item_id = 2
        testTimeMod.setUp(self)


class testMeasure4Note4(testTimeMod):

    def setUp(self):
        self.actual = 7
        self.normal = 4
        self.measure_id = 4
        self.item_id = 3
        testTimeMod.setUp(self)


class testMeasure4Note5(testTimeMod):

    def setUp(self):
        self.actual = 7
        self.normal = 4
        self.measure_id = 4
        self.item_id = 4
        testTimeMod.setUp(self)


class testMeasure4Note6(testTimeMod):

    def setUp(self):
        self.actual = 7
        self.normal = 4
        self.measure_id = 4
        self.item_id = 5
        testTimeMod.setUp(self)


class testMeasure4Note7(testTimeMod):

    def setUp(self):
        self.actual = 7
        self.normal = 4
        self.measure_id = 4
        self.item_id = 6
        testTimeMod.setUp(self)


class testMeasure4Note8(testTimeMod):

    def setUp(self):
        self.actual = 7
        self.normal = 4
        self.measure_id = 4
        self.item_id = 6
        testTimeMod.setUp(self)


class testMeasure5Note1(testTimeMod):

    def setUp(self):
        self.actual = 8
        self.normal = 8
        self.measure_id = 5
        self.item_id = 0
        self.notation_id = 0
        self.type = "start"
        self.bracket = False
        testTimeMod.setUp(self)


class testMeasure5Note2(testTimeMod):

    def setUp(self):
        self.actual = 8
        self.normal = 8
        self.measure_id = 5
        self.item_id = 1
        testTimeMod.setUp(self)


class testMeasure5Note3(testTimeMod):

    def setUp(self):
        self.actual = 8
        self.normal = 8
        self.measure_id = 5
        self.item_id = 2
        testTimeMod.setUp(self)


class testMeasure5Note4(testTimeMod):

    def setUp(self):
        self.actual = 8
        self.normal = 8
        self.measure_id = 5
        self.item_id = 3
        testTimeMod.setUp(self)


class testMeasure5Note5(testTimeMod):

    def setUp(self):
        self.actual = 8
        self.normal = 8
        self.measure_id = 5
        self.item_id = 4
        testTimeMod.setUp(self)


class testMeasure5Note6(testTimeMod):

    def setUp(self):
        self.actual = 8
        self.normal = 8
        self.measure_id = 5
        self.item_id = 5
        testTimeMod.setUp(self)


class testMeasure5Note7(testTimeMod):

    def setUp(self):
        self.actual = 8
        self.normal = 8
        self.measure_id = 5
        self.item_id = 6
        testTimeMod.setUp(self)


class testMeasure5Note8(testTimeMod):

    def setUp(self):
        self.actual = 8
        self.normal = 8
        self.measure_id = 5
        self.item_id = 7
        self.notation_id = 0
        self.type = "stop"
        testTimeMod.setUp(self)


class testMeasure6Note1(testTimeMod):

    def setUp(self):
        self.actual = 9
        self.normal = 8
        self.measure_id = 6
        self.item_id = 0
        self.notation_id = 0
        self.type = "start"
        self.bracket = False
        testTimeMod.setUp(self)


class testMeasure6Note2(testTimeMod):

    def setUp(self):
        self.actual = 9
        self.normal = 8
        self.measure_id = 6
        self.item_id = 1
        testTimeMod.setUp(self)


class testMeasure6Note3(testTimeMod):

    def setUp(self):
        self.actual = 9
        self.normal = 8
        self.measure_id = 6
        self.item_id = 2
        testTimeMod.setUp(self)


class testMeasure6Note4(testTimeMod):

    def setUp(self):
        self.actual = 9
        self.normal = 8
        self.measure_id = 6
        self.item_id = 3
        testTimeMod.setUp(self)


class testMeasure6Note5(testTimeMod):

    def setUp(self):
        self.actual = 9
        self.normal = 8
        self.measure_id = 6
        self.item_id = 4
        testTimeMod.setUp(self)


class testMeasure6Note6(testTimeMod):

    def setUp(self):
        self.actual = 9
        self.normal = 8
        self.measure_id = 6
        self.item_id = 5
        testTimeMod.setUp(self)


class testMeasure6Note7(testTimeMod):

    def setUp(self):
        self.actual = 9
        self.normal = 8
        self.measure_id = 6
        self.item_id = 6
        testTimeMod.setUp(self)


class testMeasure6Note8(testTimeMod):

    def setUp(self):
        self.actual = 9
        self.normal = 8
        self.measure_id = 6
        self.item_id = 7
        testTimeMod.setUp(self)


class testMeasure6Note9(testTimeMod):

    def setUp(self):
        self.actual = 9
        self.normal = 8
        self.measure_id = 6
        self.item_id = 8
        self.notation_id = 0
        self.type = "stop"
        testTimeMod.setUp(self)
