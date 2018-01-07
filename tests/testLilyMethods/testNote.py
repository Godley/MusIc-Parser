from museparse.classes.ObjectHierarchy.ItemClasses import Directions, Note, Mark, Ornaments
from museparse.tests.testLilyMethods.lily import Lily
from museparse.classes.ObjectHierarchy.TreeClasses.MeasureNode import MeasureNode
from museparse.classes.ObjectHierarchy.TreeClasses.StaffNode import StaffNode


class testNote(Lily):

    def setUp(self):
        self.item = Note.Note()
        self.lilystring = ""
        Lily.setUp(self)


class testNoteWithType(Lily):

    def setUp(self):
        self.item = Note.Note(type="eighth")
        self.lilystring = "8"
        Lily.setUp(self)


class testNoteWithDot(Lily):

    def setUp(self):
        self.item = Note.Note(type="eighth", dots=1)
        self.lilystring = "8."
        Lily.setUp(self)


class testNoteWithDoubleDot(Lily):

    def setUp(self):
        self.item = Note.Note(type="eighth", dots=2)
        self.lilystring = "8.."
        Lily.setUp(self)


class testNotePitch(Lily):

    def setUp(self):
        self.item = Note.Note()
        self.item.pitch = Note.Pitch()
        self.lilystring = "c'"
        Lily.setUp(self)
        self.compile = True
        self.wrappers = ["\\new Staff{", "}"]
        self.name = "notepitch"


class testNoteWithCaesura(Lily):

    def setUp(self):
        self.item = Note.Note()
        self.item.pitch = Note.Pitch()
        self.item.add_notation(Mark.Caesura())
        self.lilystring = "\override BreathingSign.text = \markup { \musicglyph #\"scripts.caesura.curved\" } c'\\breathe "


class testNoteBeaming(Lily):

    def setUp(self):
        self.item = Note.Note()
        self.item.pitch = Note.Pitch()
        self.item.add_beam(1, Note.Beam("begin"))
        self.lilystring = "c'["

        Lily.setUp(self)
        self.compile = True
        self.wrappers = ["\\new Staff{", "}"]
        self.name = "notepitch"


class testNoteDurationQuaver(Lily):

    def setUp(self):
        self.item = Note.Note(duration=2, divisions=4)
        self.item.pitch = Note.Pitch()
        self.lilystring = "c'8"
        Lily.setUp(self)
        self.compile = True
        self.wrappers = ["\\new Staff{", "}"]
        self.name = "notedurationquaver"


class testNoteDurationMinim(Lily):

    def setUp(self):
        self.item = Note.Note(duration=8, divisions=4)
        self.item.pitch = Note.Pitch()
        self.lilystring = "c'2"
        Lily.setUp(self)
        self.compile = True
        self.wrappers = ["\\new Staff{", "}"]
        self.name = "notedurationminim"


class testNoteDurationSemiBreve(Lily):

    def setUp(self):
        self.item = Note.Note(duration=16, divisions=4)
        self.item.pitch = Note.Pitch()
        self.lilystring = "c'1"
        Lily.setUp(self)
        self.compile = True
        self.wrappers = ["\\new Staff{", "}"]
        self.name = "notedurationsemibreve"


class testNoteDurationBreve(Lily):

    def setUp(self):
        self.item = Note.Note(duration=32, divisions=4)
        self.item.pitch = Note.Pitch()
        self.lilystring = "c'\\breve"
        Lily.setUp(self)
        self.compile = True
        self.wrappers = ["\\new Staff{", "}"]
        self.name = "notedurationbreve"


class testNoteRest(Lily):

    def setUp(self):
        self.item = Note.Note(duration=4, divisions=4, rest=True)
        self.item.pitch = Note.Pitch()
        self.lilystring = "r4"
        Lily.setUp(self)
        self.compile = True
        self.wrappers = ["\\new Staff{", "}"]
        self.name = "noterest"


class testNoteTuplet(Lily):

    def setUp(self):
        self.item = Note.Note()
        self.item.pitch = Note.Pitch()
        self.item.timeMod = Note.TimeModifier(normal=2, actual=3)
        self.item.add_notation(Note.Tuplet(type="start"))
        self.lilystring = "\\tuplet 3/2 {c'"
        Lily.setUp(self)
        self.compile = True
        self.wrappers = ["\\new Staff{", "}}"]
        self.name = "notetuplet"


class testHiddenNote(Lily):

    def setUp(self):
        self.item = Note.Note()
        self.item.pitch = Note.Pitch()
        self.item.print = False
        Lily.setUp(self)
        self.compile = True
        self.wrappers = ["\\new Staff{a8 ", " c'8]}"]
        self.lilystring = "\n\hideNotes\nc'\n\\unHideNotes"
        self.name = "notebeamstart"


class testNoteBeam(Lily):

    def setUp(self):
        self.item = Note.Note()
        self.item.pitch = Note.Pitch()
        self.item.add_beam(1, Note.Beam("begin"))
        Lily.setUp(self)
        self.compile = True
        self.wrappers = ["\\new Staff{a8 ", "c'8]}"]
        self.lilystring = "c'["
        self.name = "notebeamstart"


class testNoteMultipleBeam(Lily):

    def setUp(self):
        self.item = Note.Note()
        self.item.pitch = Note.Pitch()
        self.item.add_beam(1, Note.Beam("end"))
        self.item.add_beam(2, Note.Beam("begin"))
        Lily.setUp(self)
        self.wrappers = ["\\new Staff{a8 ", "c'8]}"]
        self.lilystring = "c']["
        self.name = "notebeamstart"


class testStaffWithNoEndBeams(Lily):

    def setUp(self):
        self.item = StaffNode()
        self.item.AddChild(MeasureNode(), 1)
        measure = self.item.GetChild(1)
        note = Note.Note()
        note.pitch = Note.Pitch()
        note.add_beam(2, Note.Beam("begin"))
        measure.addNote(note)
        self.item.NewBeam("begin")
        Lily.setUp(self)
        self.lilystring = " % measure 1\nc'  | \n\n"
        self.name = "notenoendbeam"


class testNoteContinue(Lily):

    def setUp(self):
        self.item = Note.Note()
        self.item.pitch = Note.Pitch()
        self.item.add_beam(1, Note.Beam("continue"))
        Lily.setUp(self)
        self.compile = True
        self.wrappers = ["\\new Staff{a [c'8", "8]}"]
        self.lilystring = "c'"
        self.name = "notebeamcont"


class testNoteStop(Lily):

    def setUp(self):
        self.item = Note.Note()
        self.item.pitch = Note.Pitch()
        self.item.add_beam(1, Note.Beam("end"))
        Lily.setUp(self)
        self.compile = True
        self.wrappers = ["\\new Staff{a [", "}"]
        self.lilystring = "c']"
        self.name = "notebeamend"


class testNotehead(Lily):

    def setUp(self):
        self.item = Note.Note()
        self.item.pitch = Note.Pitch()
        self.item.notehead = Note.Notehead(type="diamond")
        Lily.setUp(self)
        self.compile = True
        self.wrappers = ["\\new Staff{", "}"]
        self.lilystring = "c'\\harmonic"
        self.name = "notehead"


class testGraceNote(Lily):

    def setUp(self):
        self.item = Note.Note()
        self.item.pitch = Note.Pitch()
        self.item.add_notation(Note.GraceNote(first=True))
        Lily.setUp(self)
        self.compile = True
        self.wrappers = ["\\new Staff{", "}}"]
        self.lilystring = "\grace { c'"
        self.name = "notegrace"


class testGraceNoteSlash(Lily):

    def setUp(self):
        self.item = Note.Note()
        self.item.pitch = Note.Pitch()
        self.item.add_notation(Note.GraceNote(slash=True, first=True))
        Lily.setUp(self)
        self.compile = True
        self.wrappers = ["\\new Staff{", "}}"]
        self.lilystring = "\slashedGrace { c'"
        self.name = "notegrace"


class testGraceNoteContinue(Lily):

    def setUp(self):
        self.item = Note.Note()
        self.item.pitch = Note.Pitch()
        self.item.add_notation(Note.GraceNote(slash=True))
        Lily.setUp(self)
        self.compile = True
        self.wrappers = ["\\new Staff{", "}}"]
        self.lilystring = " c'"
        self.name = "notegrace"


class testChordNoteStart(Lily):

    def setUp(self):
        self.item = Note.Note(chord="start")
        self.item.pitch = Note.Pitch()
        Lily.setUp(self)
        self.compile = True
        self.wrappers = ["\\new Staff{", ">}"]
        self.lilystring = "<c'"
        self.name = "notechord"


class testChordNoteContinue(Lily):

    def setUp(self):
        self.item = Note.Note(chord="continue")
        self.item.pitch = Note.Pitch()
        Lily.setUp(self)
        self.compile = True
        self.wrappers = ["\\new Staff{", "}"]
        self.lilystring = "c'"
        self.name = "chordcont"


class testChordNoteEnd(Lily):

    def setUp(self):
        self.item = Note.Note(chord="stop")
        self.item.pitch = Note.Pitch()
        Lily.setUp(self)
        self.compile = True
        self.wrappers = ["\\new Staff{<", "}"]
        self.lilystring = "c'>"
        self.name = "notecordstop"


class testNoteArpeggiate(Lily):

    def setUp(self):
        self.item = Note.Note()
        self.item.pitch = Note.Pitch()
        self.item.add_notation(Note.Arpeggiate(type="start"))
        self.item.add_notation(Note.Arpeggiate(type="stop"))
        Lily.setUp(self)
        self.compile = True
        self.wrappers = ["\\new Staff{", "}"]
        self.lilystring = "\\arpeggioNormal  c'\\arpeggio"
        self.name = "notearpeggiate"


class testNoteNonArpeggiate(Lily):

    def setUp(self):
        self.item = Note.Note()
        self.item.pitch = Note.Pitch()
        self.item.add_notation(Note.NonArpeggiate(type="start"))
        self.item.add_notation(Note.NonArpeggiate(type="stop"))
        Lily.setUp(self)
        self.compile = True
        self.wrappers = ["\\new Staff{", "}"]
        self.lilystring = "\\arpeggioBracket  c'\\arpeggio"
        self.name = "notenonarpegg"


class testGliss(Lily):

    def setUp(self):
        self.item = Note.Note()
        self.item.pitch = Note.Pitch()
        self.item.add_notation(Note.Glissando())
        Lily.setUp(self)
        self.compile = True
        self.wrappers = ["\\new Staff{", "}"]
        self.lilystring = "\\override Glissando.style = #'zigzag c'\glissando"
        self.name = "notegliss"


class testSlide(Lily):

    def setUp(self):
        self.item = Note.Note()
        self.item.pitch = Note.Pitch()
        self.item.add_notation(Note.Slide())
        Lily.setUp(self)
        self.compile = True
        self.wrappers = ["\\new Staff{", "}"]
        self.lilystring = "c'\glissando"
        self.name = "noteslide"


class testSlideStop(Lily):

    def setUp(self):
        self.item = Note.Note()
        self.item.pitch = Note.Pitch()
        self.item.add_notation(Note.Slide(type="stop"))
        Lily.setUp(self)
        self.compile = True
        self.wrappers = ["\\new Staff{", "}"]
        self.lilystring = "c'"
        self.name = "noteslidestop"


class testNoteMordent(Lily):

    def setUp(self):
        self.item = Note.Note()
        self.item.pitch = Note.Pitch()
        self.item.add_notation(Ornaments.Mordent())
        self.lilystring = "c'\mordent"
        Lily.setUp(self)
        self.compile = True
        self.wrappers = ["\\new Staff{", "}"]
        self.name = "notemordent"


class testNoteInvMordent(Lily):

    def setUp(self):
        self.item = Note.Note()
        self.item.pitch = Note.Pitch()
        self.item.add_notation(Ornaments.InvertedMordent())
        self.lilystring = "c'\prall"
        Lily.setUp(self)
        self.compile = True
        self.wrappers = ["\\new Staff{", "}"]
        self.name = "noteprall"


class testNoteTrill(Lily):

    def setUp(self):
        self.item = Note.Note()
        self.item.pitch = Note.Pitch()
        self.item.add_notation(Ornaments.Trill())
        self.lilystring = "c'\\trill"
        Lily.setUp(self)
        self.compile = True
        self.wrappers = ["\\new Staff{", "}"]
        self.name = "notetrill"


class testNoteTurn(Lily):

    def setUp(self):
        self.item = Note.Note()
        self.item.pitch = Note.Pitch()
        self.item.add_notation(Ornaments.Turn())
        self.lilystring = "c'\\turn"
        Lily.setUp(self)
        self.compile = True
        self.wrappers = ["\\new Staff{", "}"]
        self.name = "noteturn"


class testNoteInvTurn(Lily):

    def setUp(self):
        self.item = Note.Note()
        self.item.pitch = Note.Pitch()
        self.item.add_notation(Ornaments.InvertedTurn())
        self.lilystring = "c'\\reverseturn"
        Lily.setUp(self)
        self.compile = True
        self.wrappers = ["\\new Staff{", "}"]
        self.name = "notereverseturn"


class testNoteTremolo(Lily):

    def setUp(self):
        self.item = Note.Note()
        self.item.pitch = Note.Pitch()
        self.item.add_notation(Ornaments.Tremolo(type="start"))

        self.lilystring = "\\repeat tremolo 4 {c'"
        Lily.setUp(self)
        self.compile = True
        self.wrappers = ["\\new Staff{", "}}"]
        self.name = "notetremolo"


class testNoteSlur(Lily):

    def setUp(self):
        self.item = Note.Note()
        self.item.pitch = Note.Pitch()
        self.item.add_slur(Directions.Slur(type="start"))

        self.lilystring = "c'("


class testNoteTwoSlurs(Lily):

    def setUp(self):
        self.item = Note.Note()
        self.item.pitch = Note.Pitch()
        self.item.add_slur(Directions.Slur(type="stop"))
        self.item.add_slur(Directions.Slur(type="start"))
        self.lilystring = "c')("
        Lily.setUp(self)
