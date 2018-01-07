from museparse.classes.ObjectHierarchy.ItemClasses import Note
from museparse.classes.ObjectHierarchy.TreeClasses.MeasureNode import MeasureNode
from museparse.tests.testLilyMethods.lily import Lily


class testTie(Lily):

    def setUp(self):
        self.item = Note.Tie(None)
        self.lilystring = ""


class testTieStart(Lily):

    def setUp(self):
        self.item = Note.Tie("start")
        self.lilystring = "~"


class testTieStop(Lily):

    def setUp(self):
        self.item = Note.Tie("stop")
        self.lilystring = ""


class testNotehead(Lily):

    def setUp(self):
        self.item = Note.Notehead()
        self.lilystring = ["\n", ""]


class testNoteheadCircleX(Lily):

    def setUp(self):
        self.item = Note.Notehead(type="circle-x")
        self.lilystring = ["\n\\tweak #'style #'xcircle\n", ""]


class testNoteheadType(Lily):

    def setUp(self):
        self.item = Note.Notehead(type="diamond")
        self.lilystring = ["\\harmonic"]


class testNoteheadCross(Lily):

    def setUp(self):
        self.item = Note.Notehead(type="x")
        self.lilystring = ["\\xNote", ""]


class testStem(Lily):

    def setUp(self):
        self.item = Note.Stem(None)
        self.lilystring = "\n\stemNeutral"


class testStemUp(Lily):

    def setUp(self):
        self.item = Note.Stem("up")
        self.lilystring = "\n\stemUp"


class testStemDown(Lily):

    def setUp(self):
        self.item = Note.Stem("down")
        self.lilystring = "\n\stemDown"


class testTuplet(Lily):

    def setUp(self):
        self.item = Note.Tuplet()
        self.lilystring = "\\tuplet"


class testTupletType(Lily):

    def setUp(self):
        self.item = Note.Tuplet(type="start")
        self.lilystring = "\\tuplet"


class testTupletStop(Lily):

    def setUp(self):
        self.item = Note.Tuplet(type="stop")
        self.lilystring = "}"


class testTupletBracket(Lily):

    def setUp(self):
        self.item = Note.Tuplet(bracket=True)
        self.lilystring = "\once \override TupletBracket.bracket-visibility = ##t\n\\tuplet"


class testTupletBracketNone(Lily):

    def setUp(self):
        self.item = Note.Tuplet(bracket=False)
        self.lilystring = "\once \override TupletBracket.bracket-visibility = ##f\n\\tuplet"


class testNoteWithTimeModButNoTuplet(Lily):

    def setUp(self):
        self.item = Note.Note()
        self.item.pitch = Note.Pitch()
        self.item.timeMod = Note.TimeModifier(normal=2, actual=3, first=True)
        self.lilystring = "\once \override TupletBracket.bracket-visibility = ##f\n\omit TupletNumber\n\\tuplet 3/2 {c'"


class testMeasureWithTimeModButNoTuplet(Lily):

    def setUp(self):
        self.item = MeasureNode()
        note = Note.Note()
        note.pitch = Note.Pitch()
        note.timeMod = Note.TimeModifier(normal=2, actual=3)
        note2 = Note.Note()
        self.item.addNote(note)
        self.item.addNote(note2)
        self.item.RunVoiceChecks()

        self.lilystring = "\once \override TupletBracket.bracket-visibility = ##f\n\omit TupletNumber\n\\tuplet 3/2 {c'}   | "


class testMeasureWithMultipleNoteTimeModsButNoTuplet(Lily):

    def setUp(self):
        self.item = MeasureNode()
        note = Note.Note()
        note.pitch = Note.Pitch()
        note.timeMod = Note.TimeModifier(normal=2, actual=3)
        note2 = Note.Note()
        note2.pitch = Note.Pitch()
        note2.timeMod = Note.TimeModifier(normal=2, actual=3)
        self.item.addNote(note)
        self.item.addNote(note2)
        self.item.RunVoiceChecks()

        self.lilystring = "\once \override TupletBracket.bracket-visibility = ##f\n\omit TupletNumber\n\\tuplet 3/2 {c' c'}  | "


class testGraceNote(Lily):

    def setUp(self):
        self.item = Note.GraceNote(first=True)
        self.lilystring = ["\\grace {", ""]


class testGraceNoteSlash(Lily):

    def setUp(self):
        self.item = Note.GraceNote(slash=True, first=True)
        self.lilystring = ["\slashedGrace {", ""]


class testTimeMod(Lily):

    def setUp(self):
        self.item = Note.TimeModifier()
        self.lilystring = "/"


class testTimeModNormal(Lily):

    def setUp(self):
        self.item = Note.TimeModifier(normal=3)
        self.lilystring = "/3"


class testTimeModActual(Lily):

    def setUp(self):
        self.item = Note.TimeModifier(actual=3)
        self.lilystring = "3/"


class testTimeModNormalActual(Lily):

    def setUp(self):
        self.item = Note.TimeModifier(normal=2, actual=3)
        self.lilystring = "3/2"


class testArpeggiate(Lily):

    def setUp(self):
        self.item = Note.Arpeggiate()
        self.lilystring = [""]


class testArpeggiateDir(Lily):

    def setUp(self):
        self.item = Note.Arpeggiate(direction="up", type="start")
        self.lilystring = ["\\arpeggioArrowUp", ""]


class testArpeggiateDirDown(Lily):

    def setUp(self):
        self.item = Note.Arpeggiate(direction="down", type="start")
        self.lilystring = ["\\arpeggioArrowDown", ""]


class testNonArpeggiate(Lily):

    def setUp(self):
        self.item = Note.NonArpeggiate(type="start")
        self.lilystring = ["\\arpeggioBracket", ""]


class testSlide(Lily):

    def setUp(self):
        self.item = Note.Slide()
        self.lilystring = ["\glissando"]


class testSlideType(Lily):

    def setUp(self):
        self.item = Note.Slide(type="start")
        self.lilystring = ["\glissando"]


class testSlideStop(Lily):

    def setUp(self):
        self.item = Note.Slide(type="stop")
        self.lilystring = []


class testSlideLineType(Lily):

    def setUp(self):
        self.item = Note.Slide(lineType="wavy")
        self.lilystring = [
            "\override Glissando.style = #'zigzag",
            "\glissando"]


class testGliss(Lily):

    def setUp(self):
        self.item = Note.Glissando()
        self.lilystring = [
            "\override Glissando.style = #'zigzag",
            "\glissando"]


class testGlissType(Lily):

    def setUp(self):
        self.item = Note.Glissando(type="start")
        self.lilystring = [
            "\override Glissando.style = #'zigzag",
            "\glissando"]


class testGlissStop(Lily):

    def setUp(self):
        self.item = Note.Glissando(type="stop")
        self.lilystring = []


class testBeamStart(Lily):

    def setUp(self):
        self.item = Note.Beam("begin")
        self.lilystring = "["


class testBeamStop(Lily):

    def setUp(self):
        self.item = Note.Beam("end")
        self.lilystring = "]"
