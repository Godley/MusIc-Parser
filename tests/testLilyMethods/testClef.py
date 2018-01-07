from museparse.tests.testLilyMethods.lily import Lily
from museparse.classes.ObjectHierarchy.TreeClasses import PartNode
from museparse.classes.ObjectHierarchy.ItemClasses import Clef


class testClef(Lily):

    def setUp(self):
        self.item = Clef.Clef()
        self.lilystring = ""


class testClefGG(Lily):

    def setUp(self):
        self.item = Clef.Clef(sign="GG")
        self.lilystring = "\clef GG"


class testClefSoprano(Lily):

    def setUp(self):
        self.item = Clef.Clef(sign="c", line=1)
        self.lilystring = "\clef soprano"


class testCleftenorG(Lily):

    def setUp(self):
        self.item = Clef.Clef(sign="tenorG")
        self.lilystring = "\clef tenorG"


class testClefmezzoSop(Lily):

    def setUp(self):
        self.item = Clef.Clef(sign="C", line=2)
        self.lilystring = "\clef mezzosoprano"


class testClefC(Lily):

    def setUp(self):
        self.item = Clef.Clef(sign="C")
        self.lilystring = "\clef C"


class testClefAlto(Lily):

    def setUp(self):
        self.item = Clef.Clef(sign="C", line=3)
        self.lilystring = "\clef alto"


class testClefTenor(Lily):

    def setUp(self):
        self.item = Clef.Clef(sign="C", line=4)
        self.lilystring = "\clef tenor"


class testClefBaritone(Lily):

    def setUp(self):
        self.item = Clef.Clef(sign="C", line=5)
        self.lilystring = "\clef baritone"


class testClefVarC(Lily):

    def setUp(self):
        self.item = Clef.Clef(sign="varC")
        self.lilystring = "\clef varC"


class testClefAltoVarC(Lily):

    def setUp(self):
        self.item = Clef.Clef(sign="varC", line=3)
        self.lilystring = "\clef altovarC"


class testCleftenorVarC(Lily):

    def setUp(self):
        self.item = Clef.Clef(sign="varC", line=4)
        self.lilystring = "\clef tenorvarC"


class testClefBariVarC(Lily):

    def setUp(self):
        self.item = Clef.Clef(sign="varC", line=5)
        self.lilystring = "\clef baritonevarC"


class testClefvarBaritone(Lily):

    def setUp(self):
        self.item = Clef.Clef(sign="F", line=3)
        self.lilystring = "\clef varbaritone"


class testClefF(Lily):

    def setUp(self):
        self.item = Clef.Clef(sign="F")
        self.lilystring = "\clef F"


class testClefBass(Lily):

    def setUp(self):
        self.item = Clef.Clef(sign="F", line=4)
        self.lilystring = "\clef bass"


class testClefSubbass(Lily):

    def setUp(self):
        self.item = Clef.Clef(sign="F", line=5)
        self.lilystring = "\clef subbass"


class testClefPercussion(Lily):

    def setUp(self):
        self.item = Clef.Clef(sign="percussion")
        self.lilystring = "\clef percussion"


class testClefTab(Lily):

    def setUp(self):
        self.item = Clef.Clef(sign="TAB")
        self.lilystring = "\clef moderntab"


class testClefTabInMeasure(Lily):

    def setUp(self):
        self.item = PartNode.PartNode()
        self.item.addEmptyMeasure(1, 1)
        self.item.getMeasure(1, 1).clef = Clef.Clef(sign="TAB")
        self.item.CheckIfTabStaff()
        self.lilystring = [
            "zerostaffone = \\new Staff{ % measure 1\n\clef moderntab  | \n\n }\n\n",
            "\\zerostaffone"]


class testClefTabInMeasureWithMultiClefs(Lily):

    def setUp(self):
        self.item = PartNode.PartNode()
        self.item.addEmptyMeasure(1, 1)
        self.item.getMeasure(1, 1).clef = Clef.Clef(sign="TAB")
        self.item.addEmptyMeasure(2, 1)
        self.item.getMeasure(2, 1).clef = Clef.Clef(sign="F", line=4)
        self.item.CheckIfTabStaff()
        self.lilystring = [
            "zerostaffone = \\new Staff{ % measure 1\n\clef moderntab  | \n\n % measure 2\n\clef bass  | \n\n }\n\n",
            "\\zerostaffone"]
