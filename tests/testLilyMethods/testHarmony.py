from museparse.tests.testLilyMethods.lily import Lily
from museparse.classes.ObjectHierarchy.ItemClasses import Harmony


class testHarmony(Lily):

    def setUp(self):
        self.item = Harmony.Harmony()
        self.lilystring = "\chords {\n\r}"


class testHarmonyRoot(Lily):

    def setUp(self):
        self.item = Harmony.Harmony(root="G")
        self.lilystring = "\chords {\n\rG\n\r}"


class testHarmonyBass(Lily):

    def setUp(self):
        self.item = Harmony.Harmony(bass="F")
        self.lilystring = "\chords {\n\r:/F\n\r}"


class testDegree(Lily):

    def setUp(self):
        self.item = Harmony.Degree()
        self.lilystring = ""


class testDegreeAlter(Lily):

    def setUp(self):
        self.item = Harmony.Degree(alter=1)
        self.lilystring = ""


class testDegreeValue(Lily):

    def setUp(self):
        self.item = Harmony.Degree(value=1)
        self.lilystring = "1"


class testDegreeType(Lily):

    def setUp(self):
        self.item = Harmony.Degree(type="subtract")
        self.lilystring = "no "


class testDegreeAdd(Lily):

    def setUp(self):
        self.item = Harmony.Degree(type="add")
        self.lilystring = "add "


class testDegreeTypeAlter(Lily):

    def setUp(self):
        self.item = Harmony.Degree(type="alter")
        self.lilystring = "#"


class testKindDegree(Lily):

    def setUp(self):
        self.item = Harmony.Harmony()
        self.item.kind = Harmony.Kind(parenthesis=True)
        self.item.degrees.append(Harmony.Degree(value=3))
        self.lilystring = "\\chords {\n\r:(3)\n\r}"


class testHarmonyDegrees(Lily):

    def setUp(self):
        self.item = Harmony.Harmony()
        self.item.degrees.append(Harmony.Degree())
        self.lilystring = "\chords {\n\r:\n\r}"


class testHarmonyKind(Lily):

    def setUp(self):
        self.item = Harmony.Harmony()
        self.item.kind = Harmony.Kind()
        self.lilystring = "\chords {\n\r:\n\r}"


class testHarmonyFrame(Lily):

    def setUp(self):
        self.item = Harmony.Harmony()
        self.item.frame = Harmony.Frame()
        self.lilystring = ["\chords {\n\r}",
                           "^\markup {\n\r\\fret-diagram #\"\"\n}"]


class testKind(Lily):

    def setUp(self):
        self.item = Harmony.Kind()
        self.lilystring = ""


class testKindVal(Lily):

    def setUp(self):
        self.item = Harmony.Kind(value=1)
        self.lilystring = "1"


class testKindText(Lily):

    def setUp(self):
        self.item = Harmony.Kind(text="3")
        self.lilystring = "3"


class testKindTextOverridesVal(Lily):

    def setUp(self):
        self.item = Harmony.Kind(text="3", value=2)
        self.lilystring = "3"


class testFrameNote(Lily):

    def setUp(self):
        self.item = Harmony.FrameNote()
        self.lilystring = "-"


class testFrameNoteString(Lily):

    def setUp(self):
        self.item = Harmony.FrameNote(string=1)
        self.lilystring = "1-"


class testFrameNoteFret(Lily):

    def setUp(self):

        self.item = Harmony.FrameNote(fret=1)
        self.lilystring = "-1"


class testFrame(Lily):

    def setUp(self):
        self.item = Harmony.Frame()
        self.lilystring = "^\markup {\n\r\\fret-diagram #\"\"\n}"


class testFrameStrings(Lily):

    def setUp(self):
        self.item = Harmony.Frame(strings=6)
        self.lilystring = "^\markup {\n\r\\fret-diagram #\"w:6;6-o;5-o;4-o;3-o;2-o;1-o;\"\n}"


class testFrameFrets(Lily):

    def setUp(self):
        self.item = Harmony.Frame(frets=6)
        self.lilystring = "^\markup {\n\r\\fret-diagram #\"h:6;\"\n}"


class testFrameWithNote(Lily):

    def setUp(self):
        self.item = Harmony.Frame(
            strings=6, notes={
                1: Harmony.FrameNote(
                    fret=3)})
        self.lilystring = "^\markup {\n\r\\fret-diagram #\"w:6;6-o;5-o;4-o;3-o;2-o;1-3;\"\n}"


class testFrameBarre(Lily):

    def setUp(self):
        self.item = Harmony.Frame(
            strings=6, notes={
                2: Harmony.FrameNote(
                    fret=1)})
        self.item.notes[2].barre = "stop"
        self.item.notes[3] = Harmony.FrameNote(fret=1)
        self.item.notes[3].barre = "start"
        self.lilystring = "^\markup {\n\r\\fret-diagram #\"w:6;6-o;5-o;4-o;3-1-2;2-1;1-o;\"\n}"
