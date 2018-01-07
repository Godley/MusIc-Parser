from museparse.tests.testLilyMethods.lily import Lily
from museparse.classes.ObjectHierarchy.ItemClasses import Note


class testPitch(Lily):

    def setUp(self):
        self.item = Note.Pitch()
        self.lilystring = "c'"


class testPitchAlter(Lily):

    def setUp(self):
        self.item = Note.Pitch(alter=1)
        self.lilystring = "cis'"


class testPitchOctave(Lily):

    def setUp(self):
        self.item = Note.Pitch(octave=2)
        self.lilystring = "c,"


class testPitchStep(Lily):

    def setUp(self):
        self.item = Note.Pitch(step="A")
        self.lilystring = "a'"


class testPitchDubSharp(Lily):

    def setUp(self):
        self.item = Note.Pitch(accidental="double-sharp")
        self.lilystring = "cisis'"


class testPitchDubFlat(Lily):

    def setUp(self):
        self.item = Note.Pitch(accidental="flat-flat")
        self.lilystring = "ceses'"


class testPitchNatural(Lily):

    def setUp(self):
        self.item = Note.Pitch(accidental="natural")
        self.lilystring = "c'"


class testPitchQuarterFlat(Lily):

    def setUp(self):
        self.item = Note.Pitch(accidental="quarter-flat")
        self.lilystring = "ceh'"


class testPitchThreeQuarterFlat(Lily):

    def setUp(self):
        self.item = Note.Pitch(accidental="three-quarters-flat")
        self.lilystring = "ceseh'"


class testPitchQuarterSharp(Lily):

    def setUp(self):
        self.item = Note.Pitch(accidental="quarter-sharp")
        self.lilystring = "cih'"


class testPitchThreeQuarterSharp(Lily):

    def setUp(self):
        self.item = Note.Pitch(accidental="three-quarters-sharp")
        self.lilystring = "cisih'"
