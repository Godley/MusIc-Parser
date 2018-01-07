import os

from museparse.tests.testUsingXML.xmlSet import xmlSet, parsePiece
from museparse.classes.ObjectHierarchy.ItemClasses import Directions
from museparse.classes.ObjectHierarchy.TreeClasses.PartNode import PartNode
from museparse.classes.ObjectHierarchy.TreeClasses.MeasureNode import MeasureNode
from museparse.classes.ObjectHierarchy.TreeClasses.BaseTree import Search
from museparse.classes.ObjectHierarchy.TreeClasses.NoteNode import NoteNode
from museparse.classes.ObjectHierarchy.TreeClasses.OtherNodes import DirectionNode
from museparse.SampleMusicXML import testcases


partname = "text.xml"
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


class testCredit(xmlSet):

    def setUp(self):
        xmlSet.setUp(self)
        if hasattr(self, "note_id"):
            if self.note_id in piece.GetItem().meta.credits:
                self.item = piece.GetItem().meta.credits[self.note_id]

    def testHasCredits(self):
        meta = piece.GetItem().meta
        self.assertTrue(hasattr(meta, "credits"))

    def testCredOne(self):
        if hasattr(self, "item"):
            if hasattr(self, "type"):
                self.assertIsInstance(self.item, self.type)
            else:
                self.assertIsInstance(self.item, Directions.CreditText)

    def testVal(self):
        if hasattr(self, "item"):
            self.assertEqual(self.value, self.item.text)

    def testPos(self):
        if hasattr(self, "item"):
            self.assertEqual(self.x, self.item.x)
            self.assertEqual(self.y, self.item.y)

    def testSize(self):
        if hasattr(self, "item"):
            self.assertEqual(self.size, self.item.size)

    def testJustify(self):
        if hasattr(self, "item"):
            self.assertEqual(self.justify, self.item.justify)

    def testValign(self):
        if hasattr(self, "item"):
            self.assertEqual(self.valign, self.item.valign)

    def testPage(self):
        if hasattr(self, "item"):
            self.assertEqual(self.page, self.item.page)


class testDirection(xmlSet):

    def setUp(self):
        self.p_id = "P1"
        if hasattr(self, "measure_id"):
            self.measure = piece.getPart(
                self.p_id).getMeasure(
                self.measure_id, 1)

        if hasattr(self, "item_id"):
            note = Search(NoteNode, self.measure, 1)
            self.item = Search(DirectionNode, note, self.item_id + 1).GetItem()

    def testInstance(self):
        if hasattr(self, "item"):
            self.assertIsInstance(self.item, Directions.Direction)

    def testPlacement(self):
        if hasattr(self, "item"):
            self.assertEqual(self.placement, self.item.placement)

    def testVal(self):
        if hasattr(self, "item"):
            self.assertEqual(self.words, self.item.text)


class testRehearsal(testDirection):

    def testInstance(self):
        if hasattr(self, "item"):
            self.assertIsInstance(self.item, Directions.RehearsalMark)


class testLyric(xmlSet):

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

    def testExists(self):
        if hasattr(self, "item"):
            self.assertTrue(hasattr(self.item, "lyrics"))

    def testInDict(self):
        if hasattr(self, "item"):
            self.assertTrue(self.number in self.item.lyrics)

    def testInstance(self):
        if hasattr(self, "item"):
            self.assertIsInstance(
                self.item.lyrics[
                    self.number],
                Directions.Lyric)

    def testSyllable(self):
        if hasattr(self, "item"):
            self.assertEqual(
                self.syllable, self.item.lyrics[
                    self.number].syllabic)

    def testText(self):
        if hasattr(self, "item"):
            self.assertEqual(self.text, self.item.lyrics[self.number].text)


class testCreditOne(testCredit):

    def setUp(self):
        self.note_id = 0
        self.x = 56.6929
        self.y = 1560.09
        self.size = 12
        self.justify = "left"
        self.valign = "top"
        self.value = "Charlotte Godley"
        self.page = 1
        testCredit.setUp(self)


class testCreditTwo(xmlSet):

    def setUp(self):
        self.note_id = 1
        self.x = 595.276
        self.y = 1627.09
        self.size = 24
        self.justify = "center"
        self.valign = "top"
        self.value = "Hello Friends"
        self.page = 1
        xmlSet.setUp(self)
        self.item = piece.GetItem().meta.title
        self.type = str

    def testVal(self):
        self.assertEqual(self.item, self.value)


class testCreditThree(xmlSet):

    def setUp(self):
        self.note_id = 2
        self.x = 1133.86
        self.y = 1560.09
        self.size = 12
        self.justify = "right"
        self.valign = "top"
        self.value = "Charlotte Godley"
        self.page = 1
        xmlSet.setUp(self)
        self.item = piece.GetItem().meta.composer
        self.type = str

    def testVal(self):
        self.assertEqual(self.item, self.value)


class testMeasureTwo(testDirection):

    def setUp(self):
        self.measure_id = 2
        self.item_id = 0
        self.placement = "above"
        self.words = "blablabla"
        testDirection.setUp(self)


class testMeasureFive(testRehearsal):

    def setUp(self):
        self.measure_id = 5
        self.item_id = 0
        self.words = "B"
        self.placement = "above"
        testRehearsal.setUp(self)


class testMeasureSeven(testLyric):

    def setUp(self):
        self.measure_id = 7
        self.item_id = 0
        self.text = "abc"
        self.syllable = "single"
        self.number = 1
        testLyric.setUp(self)
