import os

from museparse.tests.testUsingXML.xmlSet import xmlSet, parsePiece
from museparse.classes.ObjectHierarchy.ItemClasses import Mark, Ornaments
from museparse.classes.ObjectHierarchy.TreeClasses.PartNode import PartNode
from museparse.classes.ObjectHierarchy.TreeClasses.MeasureNode import MeasureNode
from museparse.classes.ObjectHierarchy.TreeClasses.BaseTree import Search
from museparse.classes.ObjectHierarchy.TreeClasses.NoteNode import NoteNode
from museparse.SampleMusicXML import testcases


partname = "TrillsFermataOrnaments.xml"
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


class testOrnament(xmlSet):

    def setUp(self):
        xmlSet.setUp(self)
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
        if hasattr(self, "orn_id") and hasattr(self.item, "postnotation"):
            self.ornament = self.item.postnotation[self.orn_id]

    def testType(self):
        if hasattr(self, "ornament"):
            self.assertIsInstance(self.ornament, self.instance)

    def testOrnType(self):
        if hasattr(self, "type") and hasattr(self, "ornament"):
            self.assertEqual(self.type, self.ornament.type)


class testTechnique(xmlSet):

    def setUp(self):
        xmlSet.setUp(self)
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
        if hasattr(self, "orn_id"):
            self.ornament = self.item.postnotation[self.orn_id]

    def testIsTechnique(self):
        if hasattr(self, "ornament"):
            self.assertIsInstance(self.ornament, Mark.Technique)

    def testType(self):
        if hasattr(self, "ornament"):
            self.assertEqual(self.type, self.ornament.type)


class testFermata(testOrnament):

    def testSymbol(self):
        if hasattr(self, "ornament") and hasattr(self, "value"):
            self.assertEqual(self.value, self.ornament.symbol)


class testMeasure1Note1(testOrnament):

    def setUp(self):
        self.measure_id = 1
        self.item_id = 0
        self.orn_id = 0
        self.instance = Ornaments.InvertedMordent
        testOrnament.setUp(self)


class testMeasure1Note2(testOrnament):

    def setUp(self):
        self.measure_id = 1
        self.item_id = 1
        self.orn_id = 0
        self.instance = Ornaments.Trill
        testOrnament.setUp(self)


class testMeasure1Note3(testOrnament):

    def setUp(self):
        self.measure_id = 1
        self.item_id = 2
        self.orn_id = 0
        self.instance = Ornaments.InvertedTurn
        testOrnament.setUp(self)


class testMeasure1Note4(testTechnique):

    def setUp(self):
        self.measure_id = 1
        self.item_id = 3
        self.orn_id = 0
        self.type = "snap-pizzicato"
        testTechnique.setUp(self)


class testMeasure3Note3(testOrnament):

    def setUp(self):
        self.measure_id = 3
        self.item_id = 2
        self.orn_id = 0
        self.instance = Ornaments.Mordent
        testOrnament.setUp(self)


class testMeasure3Note4(testOrnament):

    def setUp(self):
        self.measure_id = 3
        self.item_id = 3
        self.orn_id = 0
        self.instance = Ornaments.InvertedMordent
        testOrnament.setUp(self)


class testMeasure4Note1(testOrnament):

    def setUp(self):
        self.measure_id = 4
        self.item_id = 0
        self.orn_id = 0
        self.instance = Ornaments.Turn
        testOrnament.setUp(self)


class testMeasure4Note2(testTechnique):

    def setUp(self):
        self.measure_id = 4
        self.item_id = 1
        self.orn_id = 0
        self.type = "down-bow"
        testTechnique.setUp(self)


class testMeasure4Note3(testTechnique):

    def setUp(self):
        self.measure_id = 4
        self.item_id = 2
        self.orn_id = 0
        self.type = "up-bow"
        testTechnique.setUp(self)


class testMeasure4Note4(testTechnique):

    def setUp(self):
        self.measure_id = 4
        self.item_id = 3
        self.orn_id = 0
        self.type = "stopped"
        testTechnique.setUp(self)


class testMeasure5Note2(testOrnament):

    def setUp(self):
        self.measure_id = 5
        self.item_id = 1
        self.orn_id = 0
        self.instance = Mark.StrongAccent
        self.type = "down"
        testOrnament.setUp(self)

    def testSymbol(self):
        self.assertEqual("V", self.ornament.symbol)


class testMeasure5Note3(testOrnament):

    def setUp(self):
        self.measure_id = 5
        self.item_id = 2
        self.orn_id = 0
        self.instance = Mark.StrongAccent
        self.type = "up"
        testOrnament.setUp(self)

    def testSymbol(self):
        self.assertEqual("^", self.ornament.symbol)


class testMeasure5Note4(testOrnament):

    def setUp(self):
        self.measure_id = 5
        self.item_id = 3
        self.orn_id = 0
        self.instance = Mark.DetachedLegato
        testOrnament.setUp(self)


class testMeasure6Note2(testOrnament):

    def setUp(self):
        self.measure_id = 6
        self.item_id = 1
        self.orn_id = 0
        self.instance = Mark.Tenuto
        testOrnament.setUp(self)


class testMeasure6Note3(testOrnament):

    def setUp(self):
        self.measure_id = 6
        self.item_id = 2
        self.orn_id = 0
        self.instance = Mark.Staccatissimo
        testOrnament.setUp(self)


class testMeasure6Note4(testOrnament):

    def setUp(self):
        self.measure_id = 6
        self.item_id = 3
        self.orn_id = 0
        self.instance = Mark.Staccatissimo
        testOrnament.setUp(self)


class testMeasure7Note1(testOrnament):

    def setUp(self):
        self.measure_id = 7
        self.item_id = 0
        self.orn_id = 0
        self.instance = Mark.Staccato
        testOrnament.setUp(self)


class testMeasure7Note3(testOrnament):

    def setUp(self):
        self.measure_id = 7
        self.item_id = 2
        self.orn_id = 0
        self.instance = Mark.Accent
        testOrnament.setUp(self)


class testMeasure8Note1(testFermata):

    def setUp(self):
        self.measure_id = 8
        self.item_id = 0
        self.orn_id = 0
        self.value = "square"
        self.type = "inverted"
        self.instance = Mark.Fermata
        testFermata.setUp(self)


class testMeasure9Note1(testFermata):

    def setUp(self):
        self.measure_id = 9
        self.item_id = 0
        self.orn_id = 0
        self.value = "angled"
        self.type = "inverted"
        self.instance = Mark.Fermata
        testFermata.setUp(self)


class testMeasure9Note2(testFermata):

    def setUp(self):
        self.measure_id = 9
        self.item_id = 1
        self.orn_id = 0
        self.value = "angled"
        self.type = "upright"
        self.instance = Mark.Fermata
        testFermata.setUp(self)


class testMeasure9Note3(testFermata):

    def setUp(self):
        self.measure_id = 9
        self.item_id = 2
        self.orn_id = 0
        self.type = "inverted"
        self.instance = Mark.Fermata
        testFermata.setUp(self)


class testMeasure9Note4(testFermata):

    def setUp(self):
        self.measure_id = 9
        self.item_id = 3
        self.orn_id = 0
        self.type = "upright"
        self.instance = Mark.Fermata
        testFermata.setUp(self)
