from museparse.tests.testLilyMethods.lily import Lily
from museparse.classes.ObjectHierarchy.ItemClasses import Mark


class testNotation(Lily):

    def setUp(self):
        self.item = Mark.Notation()
        self.lilystring = "\\"


class testAccent(Lily):

    def setUp(self):
        self.item = Mark.Accent()
        self.lilystring = "\\accent "


class testStrongAccent(Lily):

    def setUp(self):
        self.item = Mark.StrongAccent()
        self.lilystring = "\marcato "


class testStaccato(Lily):

    def setUp(self):
        self.item = Mark.Staccato()
        self.lilystring = "\staccato "


class testStaccatissimo(Lily):

    def setUp(self):
        self.item = Mark.Staccatissimo()
        self.lilystring = "\staccatissimo "


class testTenuto(Lily):

    def setUp(self):
        self.item = Mark.Tenuto()
        self.lilystring = "\\tenuto "


class testDetachedLeg(Lily):

    def setUp(self):
        self.item = Mark.DetachedLegato()
        self.lilystring = "\portato "


class testFermata(Lily):

    def setUp(self):
        self.item = Mark.Fermata()
        self.lilystring = "\\fermata "


class testShortFermata(Lily):

    def setUp(self):
        self.item = Mark.Fermata(symbol="angled")
        self.lilystring = "\\shortfermata "


class testLongFermata(Lily):

    def setUp(self):
        self.item = Mark.Fermata(symbol="square")
        self.lilystring = "\\longfermata "


class testVeryLongFermata(Lily):

    def setUp(self):
        self.item = Mark.Fermata(symbol="squared")
        self.lilystring = "\\verylongfermata "


class testBreathMark(Lily):

    def setUp(self):
        self.item = Mark.BreathMark()
        self.lilystring = [
            "\override Staff.BreathingSign.text = \markup { \musicglyph #\"scripts.rvarcomma\" }",
            "\\breathe "]


class testCaesura(Lily):

    def setUp(self):
        self.item = Mark.Caesura()

        self.lilystring = [
            "\override BreathingSign.text = \markup { \musicglyph #\"scripts.caesura.curved\" }",
            "\\breathe "]


class testTechnique(Lily):

    def setUp(self):
        self.item = Mark.Technique()
        self.lilystring = "\\"


class testUpBow(Lily):

    def setUp(self):
        self.item = Mark.Technique(type="up-bow")
        self.lilystring = "\\upbow "


class testDownBow(Lily):

    def setUp(self):
        self.item = Mark.Technique(type="down-bow")
        self.lilystring = "\downbow "


class testFingering(Lily):

    def setUp(self):
        self.item = Mark.Technique(type="fingering", symbol="1")
        self.lilystring = "-1"


class testSnapPizz(Lily):

    def setUp(self):
        self.item = Mark.Technique(type="snap-pizzicato")
        self.lilystring = "\\snappizzicato "


class testStopped(Lily):

    def setUp(self):
        self.item = Mark.Technique(type="stopped")
        self.lilystring = "\\stopped "
