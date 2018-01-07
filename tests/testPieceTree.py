import unittest

from museparse.tree import notenode, measurenode, staffnode, piecetree, basetree
from museparse.tree.partnode import PartNode


class testPieceTree(unittest.TestCase):

    def setUp(self):
        self.item = piecetree.PieceTree()

    def testAddPartGroup(self):
        part = PartNode()
        part2 = PartNode()
        self.item.AddNode(part, index="P1")
        self.item.AddNode(part2, index="P2")
        self.item.AddToGroup("wind", index="P1")
        self.item.AddToGroup("wind", index="P2")
        self.assertEqual(self.item.getGroup("wind"), ["P1", "P2"])

    def testAddPart(self):
        part = PartNode()
        self.item.AddNode(part, index="P1")
        self.assertEqual(self.item.FindNodeByIndex("P1"), part)

    def testAddInvalidMeasure(self):
        measure = measurenode.MeasureNode()
        with self.assertRaises(basetree.CannotAddToTreeException):
            self.item.AddNode(measure, index=1)

    def testFindStaff(self):
        part = PartNode()
        staff = staffnode.StaffNode()
        self.item.AddNode(part, index="P1")
        self.item.AddNode(staff, index=1)
        self.assertEqual(part.getStaff(1), staff)

    def testFindMeasure(self):
        part = PartNode()
        staff = staffnode.StaffNode()
        self.item.AddNode(part, index="P1")
        self.item.AddNode(staff, index=1)
        measure = measurenode.MeasureNode()
        self.item.AddNode(measure, index=1)
        self.assertEqual(part.getMeasure(1, 1), measure)

    def testAddMeasureOnSecondStave(self):
        part = PartNode()
        staff = staffnode.StaffNode()
        staff2 = staffnode.StaffNode()
        measure = measurenode.MeasureNode()
        self.item.AddNode(part, index="P1")
        self.item.AddNode(staff, index=1)
        self.item.AddNode(staff2, index=2)
        part.addMeasure(measure, staff=2)
        self.assertEqual(part.getMeasure(1, 2), measure)


class testAddToMeasure(unittest.TestCase):

    def setUp(self):
        self.item = piecetree.PieceTree()
        self.part = PartNode()
        self.item.AddNode(self.part, index="P1")
        self.part.addEmptyMeasure()
        self.measure = self.part.getMeasure()

    def testAddNote(self):
        note = "3"
        self.measure.addNote(note)
        voice = self.measure.getVoice(1)
        self.assertEqual(voice.GetChild(0).GetItem(), note)

    def testAddDirection(self):
        direction = "2"
        self.measure.addDirection(direction)
        voice = self.measure.getVoice(1)
        self.assertEqual(voice.GetChild(0).GetChild(1).GetItem(), direction)

    def testAddExpression(self):
        exp = "2"
        self.measure.addExpression(exp)
        voice = self.measure.getVoice(1)
        self.assertEqual(voice.GetChild(0).GetChild(0).GetItem(), exp)

    def testAddPlaceholder(self):
        self.measure.addPlaceholder()
        voice = self.measure.getVoice(1)
        self.assertEqual(voice.GetChild(0).GetItem(), None)

    def testAddNoteWithPlaceholderBeforeIt(self):
        note = 2
        self.measure.addNote(note)
        self.measure.index = 0
        self.measure.addPlaceholder()
        voice = self.measure.getVoice(1)
        self.assertEqual(voice.GetChild(0).GetItem(), None)

    def testForward(self):
        self.measure.addNote(1)
        self.measure.Forward(duration=16)
        self.assertEqual(self.measure.index, 2)

    def testBackup(self):
        self.measure.addNote(1)
        self.measure.Backup(duration=15)
        self.assertEqual(self.measure.index, 0)

    def testForwardCreatesAPlaceholder(self):
        self.measure.addNote(1)
        self.measure.Forward(duration=16)
        voice = self.measure.getVoice(1)
        self.assertIsInstance(voice.GetChild(1), notenode.NoteNode)

    def testBackupAndAddNote(self):
        self.measure.addNote(1)
        self.measure.Backup(duration=15)
        self.measure.addNote(2)
        voice = self.measure.getVoice(1)
        self.assertEqual(voice.GetChild(0).GetItem(), 2)

    def testAddDirectionThenNode(self):
        dir = 1
        note = 3
        self.measure.addDirection(dir)
        self.measure.addNote(note)
        voice = self.measure.getVoice(1)
        self.assertEqual(voice.GetChild(0).GetItem(), note)

    def testAddDirectionToSecondNote(self):
        dir = 1
        note = 2
        note1 = 3
        self.measure.addNote(note)
        self.measure.addDirection(dir)
        self.measure.addNote(note1)
        voice = self.measure.getVoice(1)
        self.assertEqual(voice.GetChild(1).GetChild(1).GetItem(), dir)

    def testAddChordNote(self):
        note = 2
        note1 = 3
        self.measure.addNote(note)
        self.measure.addNote(note1, chord=True)
        voice = self.measure.getVoice(1)
        self.assertEqual(voice.GetChild(0).GetChild(0).GetItem(), 3)

    def testAddExpressionThenChordNote(self):
        note = 2
        note1 = 3
        exp = 0
        self.measure.addNote(note)
        self.measure.addExpression(exp)
        self.measure.addNote(note1, chord=True)
        voice = self.measure.getVoice(1)
        self.assertEqual(voice.GetChild(0).GetChild(0).GetItem(), 3)

    def testLilyOutputOfPlaceholders(self):
        self.measure.addPlaceholder()
        voice = self.measure.getVoice(1)
        self.assertEqual(voice.GetChild(0).to_lily(), "")

    def testLilyOutputOfPlaceholdersWithChildren(self):
        self.measure.addPlaceholder()
        self.measure.addDirection(1)
        voice = self.measure.getVoice(1)
        self.assertEqual(voice.GetChild(0).to_lily(), "")
