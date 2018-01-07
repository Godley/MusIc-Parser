import os
import unittest

from museparse.tests.testUsingXML.xmlSet import xmlSet, parsePiece
from museparse.classes.ObjectHierarchy.TreeClasses.BaseTree import Search, FindByIndex
from museparse.classes.ObjectHierarchy.TreeClasses.NoteNode import NoteNode
from museparse.classes.ObjectHierarchy.TreeClasses.MeasureNode import MeasureNode
from museparse.classes.ObjectHierarchy.ItemClasses import Note
from museparse.SampleMusicXML import testcases


partname = "arpeggiosAndGlissandos.xml"
directory = testcases.__path__._path[0]
piece = parsePiece(os.path.join(directory, partname))


class testArpeg(xmlSet):

    def setUp(self):
        xmlSet.setUp(self)
        self.m_num = 32
        self.p_id = "P1"
        self.p_name = "Piccolo"
        self.note_num = {1: 4, 2: 4, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1, 9: 1, 10: 1,
                         11: 1, 12: 1, 13: 1, 14: 1, 15: 1, 16: 1, 17: 1, 18: 1, 19: 1,
                         20: 1, 21: 1, 22: 1, 23: 1, 24: 1, 25: 1, 26: 1, 27: 1, 28: 1,
                         29: 1, 30: 1, 31: 1, 32: 1}

    def testParts(self):
        global piece
        self.assertTrue(piece.getPart(self.p_id) is not None)
        self.assertEqual(self.p_name, piece.getPart(self.p_id).GetItem().name)

    def testMeasures(self):
        self.assertIsInstance(
            FindByIndex(
                piece.getPart(
                    self.p_id),
                self.m_num),
            MeasureNode)

    def testNotes(self):
        part = piece.getPart(self.p_id)
        staff = part.getStaff(1)
        keys = staff.GetChildrenIndexes()
        for measure in keys:
            if measure in self.note_num:
                measure_obj = part.getMeasure(measure=measure, staff=1)
                self.assertIsInstance(
                    Search(
                        NoteNode,
                        measure_obj.getVoice(1),
                        self.note_num[measure]),
                    NoteNode)


class testBar(unittest.TestCase):

    def testInstance(self):
        if hasattr(self, "instance_type"):
            self.assertIsInstance(
                self.item.wrap_notation[0],
                self.instance_type)

    def testEquality(self):
        if hasattr(self, "value"):
            self.assertEqual(self.item, self.value)


class Note1Measure1(testBar):

    def setUp(self):
        self.p_id = "P1"
        part = piece.getPart(self.p_id)
        measure = part.getMeasure(measure=1, staff=1)
        self.item = Search(NoteNode, measure, 1).GetItem()
        self.instance_type = Note.Arpeggiate


class Note2Measure1(testBar):

    def setUp(self):
        part = piece.getPart("P1")
        measure = part.getMeasure(measure=1, staff=1)
        self.item = Search(NoteNode, measure, 2).GetItem()
        self.instance_type = Note.Arpeggiate


class Note2Measure1DirectionValue(testBar):

    def setUp(self):
        self.p_id = "P1"
        part = piece.getPart(self.p_id)
        measure = part.getMeasure(measure=1, staff=1)
        note = Search(NoteNode, measure, 2).GetItem()
        self.item = note.wrap_notation[0].direction
        self.value = "up"


class Note3Measure1(testBar):

    def setUp(self):
        part = piece.getPart("P1")
        measure = part.getMeasure(measure=1, staff=1)
        self.item = Search(NoteNode, measure, 3).GetItem()
        self.instance_type = Note.Arpeggiate


class Note3Measure1DirectionValue(testBar):

    def setUp(self):
        self.p_id = "P1"
        part = piece.getPart(self.p_id)
        measure = part.getMeasure(measure=1, staff=1)
        note = Search(NoteNode, measure, 3).GetItem()
        self.item = note.wrap_notation[0].direction
        self.value = "down"


class Note4Measure1FirstNotation(testBar):

    def setUp(self):
        self.p_id = "P1"
        part = piece.getPart(self.p_id)
        measure = part.getMeasure(measure=1, staff=1)
        self.item = Search(NoteNode, measure, 4).GetItem()
        self.instance_type = Note.NonArpeggiate


class Note4Measure1SecondNotation(testBar):

    def setUp(self):
        self.p_id = "P1"
        part = piece.getPart(self.p_id)
        measure = part.getMeasure(measure=1, staff=1)
        self.item = Search(NoteNode, measure, 4).GetItem()
        self.instance_type = Note.NonArpeggiate
# TODO: fix this
# class Note4Measure1Notation1Type(testBar):
#     def setUp(self):
#         self.p_id = "P1"
#         part = piece.getPart(self.p_id)
#         measure = part.getMeasure(measure=1,staff=1)
#         self.item = Search(NoteNode, measure, 4).GetItem().wrap_notation[0].type
#         self.value = "bottom"


class Note4Measure1Notation2Type(testBar):

    def setUp(self):
        self.p_id = "P1"
        part = piece.getPart(self.p_id)
        measure = part.getMeasure(measure=1, staff=1)
        self.item = Search(
            NoteNode,
            measure,
            4).GetItem().wrap_notation[1].type
        self.value = "top"


class Note1Measure2(testBar):

    def setUp(self):
        self.p_id = "P1"
        part = piece.getPart(self.p_id)
        measure = part.getMeasure(measure=2, staff=1)
        self.item = Search(NoteNode, measure, 1).GetItem()
        self.instance_type = Note.Slide


class Note1Measure2Type(testBar):

    def setUp(self):
        self.p_id = "P1"
        part = piece.getPart(self.p_id)
        measure = part.getMeasure(measure=2, staff=1)
        self.item = Search(
            NoteNode,
            measure,
            1).GetItem().wrap_notation[0].type
        self.value = "start"


class Note1Measure2Number(testBar):

    def setUp(self):
        self.p_id = "P1"
        part = piece.getPart(self.p_id)
        measure = part.getMeasure(measure=2, staff=1)
        self.item = Search(
            NoteNode,
            measure,
            1).GetItem().wrap_notation[0].number
        self.value = 1


class Note1Measure2LineType(testBar):

    def setUp(self):
        self.p_id = "P1"
        part = piece.getPart(self.p_id)
        measure = part.getMeasure(measure=2, staff=1)
        self.item = Search(
            NoteNode,
            measure,
            1).GetItem().wrap_notation[0].lineType
        self.value = "solid"


class Note2Measure2(testBar):

    def setUp(self):
        self.p_id = "P1"
        part = piece.getPart(self.p_id)
        measure = part.getMeasure(measure=2, staff=1)
        self.item = Search(NoteNode, measure, 2).GetItem()
        self.instance_type = Note.Slide


class Note2Measure2Type(testBar):

    def setUp(self):
        self.p_id = "P1"
        part = piece.getPart(self.p_id)
        measure = part.getMeasure(measure=2, staff=1)
        self.item = Search(
            NoteNode,
            measure,
            2).GetItem().wrap_notation[0].type
        self.value = "stop"


class Note2Measure2Number(testBar):

    def setUp(self):
        self.p_id = "P1"
        part = piece.getPart(self.p_id)
        measure = part.getMeasure(measure=2, staff=1)
        self.item = Search(
            NoteNode,
            measure,
            2).GetItem().wrap_notation[0].number
        self.value = 1


class Note2Measure2LineType(testBar):

    def setUp(self):
        self.p_id = "P1"
        part = piece.getPart(self.p_id)
        measure = part.getMeasure(measure=2, staff=1)
        self.item = Search(
            NoteNode,
            measure,
            2).GetItem().wrap_notation[0].lineType
        self.value = "solid"


class Note3Measure2(testBar):

    def setUp(self):
        self.p_id = "P1"
        part = piece.getPart(self.p_id)
        measure = part.getMeasure(measure=2, staff=1)
        self.item = Search(NoteNode, measure, 3).GetItem()
        self.instance_type = Note.Glissando


class Note3Measure2Type(testBar):

    def setUp(self):
        self.p_id = "P1"
        part = piece.getPart(self.p_id)
        measure = part.getMeasure(measure=2, staff=1)
        self.item = Search(
            NoteNode,
            measure,
            3).GetItem().wrap_notation[0].type
        self.value = "start"


class Note3Measure2Number(testBar):

    def setUp(self):
        self.p_id = "P1"
        part = piece.getPart(self.p_id)
        measure = part.getMeasure(measure=2, staff=1)
        self.item = Search(
            NoteNode,
            measure,
            3).GetItem().wrap_notation[0].number
        self.value = 1


class Note3Measure2LineType(testBar):

    def setUp(self):
        self.p_id = "P1"
        part = piece.getPart(self.p_id)
        measure = part.getMeasure(measure=2, staff=1)
        self.item = Search(
            NoteNode,
            measure,
            3).GetItem().wrap_notation[0].lineType
        self.value = "wavy"


class Note4Measure2(testBar):

    def setUp(self):
        self.p_id = "P1"
        part = piece.getPart(self.p_id)
        measure = part.getMeasure(measure=2, staff=1)
        self.item = Search(NoteNode, measure, 4).GetItem()
        self.instance_type = Note.Glissando


class Note4Measure2Type(testBar):

    def setUp(self):
        self.p_id = "P1"
        part = piece.getPart(self.p_id)
        measure = part.getMeasure(measure=2, staff=1)
        self.item = Search(
            NoteNode,
            measure,
            4).GetItem().wrap_notation[0].type
        self.value = "stop"


class Note4Measure2Number(testBar):

    def setUp(self):
        self.p_id = "P1"
        part = piece.getPart(self.p_id)
        measure = part.getMeasure(measure=2, staff=1)
        self.item = Search(
            NoteNode,
            measure,
            4).GetItem().wrap_notation[0].number
        self.value = 1


class Note4Measure2LineType(testBar):

    def setUp(self):
        self.p_id = "P1"
        part = piece.getPart(self.p_id)
        measure = part.getMeasure(measure=2, staff=1)
        self.item = Search(
            NoteNode,
            measure,
            4).GetItem().wrap_notation[0].lineType
        self.value = "wavy"
