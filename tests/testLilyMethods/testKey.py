from museparse.tests.testLilyMethods.lily import Lily
from museparse.classes.ObjectHierarchy.ItemClasses import Key


class testKey(Lily):

    def setUp(self):
        self.item = Key.Key()
        self.lilystring = ""


class testKeyFifths(Lily):

    def setUp(self):
        self.item = Key.Key(fifths=1)
        self.lilystring = ""


class testKeyMode(Lily):

    def setUp(self):
        self.item = Key.Key(mode="minor")
        self.lilystring = ""


class testKeyFifthsMode(Lily):

    def setUp(self):
        self.item = Key.Key(fifths=-3, mode="minor")
        self.lilystring = "\key c \minor"


class testKeyFifthsModeFlat(Lily):

    def setUp(self):
        self.item = Key.Key(fifths=-4, mode="major")
        self.lilystring = "\key aes \major"


class testKeyFifthsModeSharp(Lily):

    def setUp(self):
        self.item = Key.Key(fifths=7, mode="major")
        self.lilystring = "\key cis \major"
