from museparse.tests.testLilyMethods.lily import Lily
from museparse.classes.ObjectHierarchy.ItemClasses import Ornaments


class testMordent(Lily):

    def setUp(self):
        self.item = Ornaments.Mordent()
        self.lilystring = "\mordent"


class testInvertedMordent(Lily):

    def setUp(self):
        self.item = Ornaments.InvertedMordent()
        self.lilystring = "\prall"


class testTrill(Lily):

    def setUp(self):
        self.item = Ornaments.Trill()
        self.lilystring = "\\trill"


class testTrillLineSpanner(Lily):

    def setUp(self):
        self.item = Ornaments.TrillSpanner(line="start")
        self.lilystring = "\\startTrillSpan\n"


class testTrillLineStopSpanner(Lily):

    def setUp(self):
        self.item = Ornaments.TrillSpanner(line="stop")
        self.lilystring = "\\stopTrillSpan\n"


class testTurn(Lily):

    def setUp(self):
        self.item = Ornaments.Turn()
        self.lilystring = "\\turn"


class testInvertedTurn(Lily):

    def setUp(self):
        self.item = Ornaments.InvertedTurn()
        self.lilystring = "\\reverseturn"


class testTremolo(Lily):

    def setUp(self):
        self.item = Ornaments.Tremolo()
        self.lilystring = "\\repeat tremolo 4 "


class testTremoloType(Lily):

    def setUp(self):
        self.item = Ornaments.Tremolo(type="single")
        self.lilystring = "\\repeat tremolo 4 "


class testTremoloVal(Lily):

    def setUp(self):
        self.item = Ornaments.Tremolo(value=2)
        self.lilystring = "\\repeat tremolo 4 "


class testTremoloTypeStart(Lily):

    def setUp(self):
        self.item = Ornaments.Tremolo(type="start")
        self.lilystring = "\\repeat tremolo 4 {"


class testTremoloTypeStop(Lily):

    def setUp(self):
        self.item = Ornaments.Tremolo(type="stop")
        self.lilystring = ["", "}"]
