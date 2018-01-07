from museparse.classes.ObjectHierarchy.ItemClasses import Note
from museparse.classes.ObjectHierarchy.TreeClasses.PartNode import PartNode
from museparse.tests.testLilyMethods.lily import Lily


class testPartMeasureWithNote(Lily):

    def setUp(self):
        self.item = PartNode()
        self.item.addEmptyMeasure(1, 1)
        measure = self.item.getMeasure(1, 1)
        note = Note.Note()
        note.pitch = Note.Pitch()
        measure.addNote(note)
        self.lilystring = [
            "zerostaffone = \\new Staff{ % measure 1\nc'  | \n\n }\n\n",
            '\\zerostaffone']


class testPartMultistafftavesWithName(Lily):

    def setUp(self):
        self.item = PartNode()
        self.item.GetItem().name = "Piano"
        self.item.addEmptyMeasure(1, 1)
        measure = self.item.getMeasure(1, 1)
        note = Note.Note()
        note.pitch = Note.Pitch()
        measure.addNote(note)
        self.item.addEmptyMeasure(1, 2)
        measure2 = self.item.getMeasure(1, 2)
        note2 = Note.Note()
        note2.pitch = Note.Pitch()
        measure2.addNote(note2)
        self.lilystring = [
            "zerostaffone = \\new Staff{ % measure 1\nc'  | \n\n }\n\nzerostafftwo = \\new Staff{ % measure 1\nc'  | \n\n }\n\n",
            "\\new StaffGroup \\with {\ninstrumentName = \markup { \n\r \column { \n\r\r \line { \"Piano\" \n\r\r } \n\r } \n } \n }<<\zerostaffone\n\zerostafftwo>>"]


class testPartMultistafftaves(Lily):

    def setUp(self):
        self.item = PartNode()
        self.item.addEmptyMeasure(1, 1)
        self.item.addEmptyMeasure(1, 2)
        measure1 = self.item.getMeasure(1, 1)
        measure2 = self.item.getMeasure(1, 2)
        note1 = Note.Note()
        note1.pitch = Note.Pitch()
        note2 = Note.Note()
        note2.pitch = Note.Pitch()
        measure1.addNote(note1)
        measure2.addNote(note2)
        self.lilystring = [
            "zerostaffone = \\new Staff{ % measure 1\nc'  | \n\n }\n\nzerostafftwo = \\new Staff{ % measure 1\nc'  | \n\n }\n\n",
            "\\new StaffGroup <<\zerostaffone\n\zerostafftwo>>"]


class testPartMultiBars(Lily):

    def setUp(self):
        self.item = PartNode()
        self.item.addEmptyMeasure(1, 1)
        self.item.addEmptyMeasure(2, 1)
        measure2 = self.item.getMeasure(2, 1)
        measure = self.item.getMeasure(1, 1)
        note = Note.Note()
        note.pitch = Note.Pitch()
        note2 = Note.Note()
        note2.pitch = Note.Pitch()
        measure.addNote(note)
        measure2.addNote(note2)
        self.lilystring = [
            "zerostaffone = \\new Staff{ % measure 1\nc'  | \n\n % measure 2\nc'  | \n\n }\n\n",
            "\\zerostaffone"]


class testPartMultiBarsstafftaves(Lily):

    def setUp(self):
        self.item = PartNode()
        self.item.addEmptyMeasure(1, 1)
        measure = self.item.getMeasure(1, 1)
        note = Note.Note()
        note.pitch = Note.Pitch()
        measure.addNote(note)
        self.item.addEmptyMeasure(1, 2)
        measure2 = self.item.getMeasure(1, 2)
        note2 = Note.Note()
        note2.pitch = Note.Pitch()
        measure2.addNote(note2)
        self.item.addEmptyMeasure(2, 1)
        measure3 = self.item.getMeasure(2, 1)
        note3 = Note.Note()
        note3.pitch = Note.Pitch()
        measure3.addNote(note3)
        self.lilystring = [
            "zerostaffone = \\new Staff{ % measure 1\nc'  | \n\n % measure 2\nc'  | \n\n }\n\nzerostafftwo = \\new Staff{ % measure 1\nc'  | \n\n }\n\n",
            "\\new StaffGroup <<\\zerostaffone\n\\zerostafftwo>>"]


class testPartWithName(Lily):

    def setUp(self):
        self.item = PartNode()
        self.item.addEmptyMeasure(1, 1)
        self.item.GetItem().name = "charlotte"
        self.lilystring = [
            "zerostaffone = \\new Staff \with {\ninstrumentName = \\markup { \n\r \\column { \n\r\r \\line { \"charlotte\" \n\r\r } \n\r } \n } \n }{ % measure 1\n | \n\n }\n\n",
            "\zerostaffone"]

    def tearDown(self):
        self.item = None
