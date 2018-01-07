from museparse.tests.testLilyMethods.lily import Lily
from museparse.classes.ObjectHierarchy.ItemClasses import Directions


class testText(Lily):

    def setUp(self):
        self.item = Directions.Text()
        self.lilystring = ""


class testTextSize(Lily):

    def setUp(self):
        self.item = Directions.Text(size=8, text="hello")
        self.lilystring = "\\abs-fontsize #8 \"hello\" "


class testTextSizeWhichIsAWord(Lily):

    def setUp(self):
        self.item = Directions.Text(size="medium", text="hello")
        self.lilystring = "\medium \"hello\" "


class testTextFont(Lily):

    def setUp(self):
        self.item = Directions.Text(font="typewriter", text="hello")
        self.lilystring = "\\typewriter \"hello\" "


class testBasicDirection(Lily):

    def setUp(self):
        self.item = Directions.Direction()
        self.lilystring = " "


class testDirectionPlacedBelow(Lily):

    def setUp(self):
        self.item = Directions.Direction(placement="below", text="hello")
        self.lilystring = " _\markup { \"hello\"  }"


class testDirectionPlacedAbove(Lily):

    def setUp(self):
        self.item = Directions.Direction(placement="above", text="hello")
        self.lilystring = " ^\markup { \"hello\"  }"


class testDirectionWithText(Lily):

    def setUp(self):
        self.item = Directions.Direction(text="whatsup")
        self.lilystring = " ^\markup { \"whatsup\"  }"


class testDirectionFont(Lily):

    def setUp(self):
        self.item = Directions.Direction(font="roman", text="lol")
        self.lilystring = " ^\markup { \\roman \"lol\"  }"


class testDirectionWithFontSize(Lily):

    def setUp(self):
        self.item = Directions.Direction(size=11, text="hello")
        self.lilystring = " ^\\markup { \\abs-fontsize #11 \"hello\"  }"


class testRehearsalMark(Lily):

    def setUp(self):
        self.item = Directions.RehearsalMark()
        self.lilystring = " \mark \default"


class testRehearsalMarkWithText(Lily):

    def setUp(self):
        self.item = Directions.RehearsalMark(text="B")
        self.lilystring = " \mark #2"


class testForward(Lily):

    def setUp(self):
        self.item = Directions.Forward()
        self.lilystring = ["percent repeat"]


class testForwardWithDuration(Lily):

    def setUp(self):
        self.item = Directions.Forward(duration=4)
        self.lilystring = ["percent repeat", 4]


class testRepeatSign(Lily):

    def setUp(self):
        self.item = Directions.RepeatSign()
        self.lilystring = " \mark  "


class testSegno(Lily):

    def setUp(self):
        self.item = Directions.RepeatSign(type="segno")
        self.lilystring = " \mark  \markup { \musicglyph #\"scripts.segno\" }"


class testCoda(Lily):

    def setUp(self):
        self.item = Directions.RepeatSign(type="coda")
        self.lilystring = " \mark  \markup { \musicglyph #\"scripts.coda\" }"


class testOctaveShift(Lily):

    def setUp(self):
        self.item = Directions.OctaveShift()
        self.lilystring = "\n\ottava #1\n"


class testOctaveShiftUp(Lily):

    def setUp(self):
        self.item = Directions.OctaveShift(amount=8)
        self.lilystring = "\n\ottava #1\n"


class testOctaveShiftDown(Lily):

    def setUp(self):
        self.item = Directions.OctaveShift(amount=15, type="down")
        self.lilystring = "\n\ottava #2\n"


class testWavyLine(Lily):

    def setUp(self):
        self.item = Directions.WavyLine()
        self.lilystring = "\startTrillSpan"


class testWavyLineStop(Lily):

    def setUp(self):
        self.item = Directions.WavyLine(type="stop")
        self.lilystring = "\stopTrillSpan"


class testPedal(Lily):

    def setUp(self):
        self.item = Directions.Pedal()
        self.lilystring = "\sustainOn\n"


class testPedalLine(Lily):

    def setUp(self):
        self.item = Directions.Pedal(line=False)
        self.lilystring = "\n\set Staff.pedalSustainStyle = #'text\n\sustainOn\n"


class testPedalType(Lily):

    def setUp(self):
        self.item = Directions.Pedal(type="start")
        self.lilystring = "\sustainOn\n"


class testPedalTypeOff(Lily):

    def setUp(self):
        self.item = Directions.Pedal(type="stop")
        self.lilystring = "\sustainOff\n"


class testBracket(Lily):

    def setUp(self):
        self.item = Directions.Bracket(type="start")
        self.lilystring = "\n\\startTextSpan\n"


class testBracketStop(Lily):

    def setUp(self):
        self.item = Directions.Bracket(type="stop")
        self.lilystring = "\n\\stopTextSpan\n"


class testBracketlType(Lily):

    def setUp(self):
        self.item = Directions.Bracket(ltype="solid")
        self.lilystring = "\override TextSpanner.dash-fraction = 1.0 \n"


class testMetronome(Lily):

    def setUp(self):
        self.item = Directions.Metronome()
        self.lilystring = ""


class testMetronomeBeat(Lily):

    def setUp(self):
        self.item = Directions.Metronome(beat="quarter")
        self.lilystring = ""


class testMetronome2Beats(Lily):

    def setUp(self):
        self.item = Directions.Metronome(beat="quarter", secondBeat="half")
        self.lilystring = " \\tempo \markup {\n\t\concat {\n\t\t\n\t\t\t\smaller \general-align #Y #DOWN \\note #\"4\" #1\n\t\t\t\t\" = \"\n\t\t\t\t\smaller \general-align #Y #DOWN \\note #\"2\" #1\n\t\t\n\t}\n}"


class testMetronomeMin(Lily):

    def setUp(self):
        self.item = Directions.Metronome(min=60)
        self.lilystring = ""


class testMetronomeBeatMin(Lily):

    def setUp(self):
        self.item = Directions.Metronome(beat="half", min=60)
        self.lilystring = " \\tempo 2=60"


class testMetronomeParenthesis(Lily):

    def setUp(self):
        self.item = Directions.Metronome(parentheses=True)
        self.lilystring = ""


class testDynamic(Lily):

    def setUp(self):
        self.item = Directions.Dynamic()
        self.lilystring = ""


class testDynamicMark(Lily):

    def setUp(self):
        self.item = Directions.Dynamic(mark="f")
        self.lilystring = "\\f"


class testWedge(Lily):

    def setUp(self):
        self.item = Directions.Wedge()
        self.lilystring = "\\"


class testWedgeType(Lily):

    def setUp(self):
        self.item = Directions.Wedge(type="crescendo")
        self.lilystring = "\<"


class testWedgeTypeDim(Lily):

    def setUp(self):
        self.item = Directions.Wedge(type="diminuendo")
        self.lilystring = "\>"


class testWedgeTypeStop(Lily):

    def setUp(self):
        self.item = Directions.Wedge(type="stop")
        self.lilystring = "\!"


class testSlur(Lily):

    def setUp(self):
        self.item = Directions.Slur()
        self.lilystring = ""


class testSlurStart(Lily):

    def setUp(self):
        self.item = Directions.Slur(type="start")
        self.lilystring = "("


class testSlurEnd(Lily):

    def setUp(self):
        self.item = Directions.Slur(type="stop")
        self.lilystring = ")"


class testCreditText(Lily):

    def setUp(self):
        self.item = Directions.CreditText(text="hello")
        self.lilystring = "\"hello\" "


class testCreditTextValign(Lily):

    def setUp(self):
        self.item = Directions.CreditText(valign="top", text="hello")
        self.lilystring = "\general-align #Y #UP\n \"hello\" "


class testCreditTextJustify(Lily):

    def setUp(self):
        self.item = Directions.CreditText(justify="right", text="hello")
        self.lilystring = "\\fill-line {\n\\null \n\override #'(baseline-skip . 4)\n\override #'(line-width . 40) {\"hello\" \n}\n\t}\n\\null\\null"


class testCreditTextCenterJustify(Lily):

    def setUp(self):
        self.item = Directions.CreditText(justify="center", text="hello")
        self.lilystring = "\\fill-line { \n \\center-column {\n\"hello\" \n}\n}"
