import unittest
import os

from museparse.classes.Output import LilypondOutput
from museparse.classes.Input import MxmlParser
from museparse.classes import Exceptions
from museparse.SampleMusicXML import testcases

folder = testcases.__path__._path[0]
import sys

# runs all testcases from start to end


class testRun(unittest.TestCase):

    def setUp(self):
        script = None
        if sys.platform == 'darwin':
            script = "~/bin/lilypond"
        if hasattr(self, "item"):
            self.lp = LilypondOutput.LilypondRenderer(
                self.item, self.file, lyscript=script)
            self.lp.run()
            self.pdf = self.file.split(".")[0] + ".pdf"

    def testRun(self):
        if hasattr(self, "file"):
            self.assertTrue(os.path.exists(self.pdf))
            if not hasattr(self, "dontcleanup"):
                self.lp.cleanup(pdf=True)


class testAccidentals(testRun):

    def setUp(self):
        self.file = os.path.join(folder, "accidentals.xml")
        parser = MxmlParser.MxmlParser()
        self.item = parser.parse(self.file)

        testRun.setUp(self)


class testActorPreludeSample(unittest.TestCase):

    def setUp(self):
        self.file = os.path.join(folder, "ActorPreludeSample.xml")

        # self.lp = LilypondOutput.LilypondRenderer(self.item, self.file, lyscript="~/bin/lilypond")
        self.pdf = self.file.split(".")[0] + ".pdf"

    def testRun(self):
        with self.assertRaises(Exceptions.DrumNotImplementedException):
            parser = MxmlParser.MxmlParser()
            self.item = parser.parse(self.file)


class testarpeggiosAndGlissandos(testRun):

    def setUp(self):
        self.file = os.path.join(folder, "arpeggiosAndGlissandos.xml")
        parser = MxmlParser.MxmlParser()
        self.item = parser.parse(self.file)
        self.dontcleanup = True
        testRun.setUp(self)


class testbarlines(testRun):

    def setUp(self):
        self.file = os.path.join(folder, "barlines.xml")
        parser = MxmlParser.MxmlParser()
        self.item = parser.parse(self.file)
        testRun.setUp(self)


class testrepeatbarlines(testRun):

    def setUp(self):
        self.file = os.path.join(folder, "repeat-barlines.xml")
        parser = MxmlParser.MxmlParser()
        self.item = parser.parse(self.file)
        testRun.setUp(self)


class testbeams(testRun):

    def setUp(self):
        self.file = os.path.join(folder, "beams.xml")
        parser = MxmlParser.MxmlParser()
        self.item = parser.parse(self.file)
        self.dontcleanup = True
        testRun.setUp(self)


class testbreathmarks(testRun):

    def setUp(self):
        self.file = os.path.join(folder, "breathMarks.xml")
        parser = MxmlParser.MxmlParser()
        self.item = parser.parse(self.file)
        self.dontcleanup = True
        testRun.setUp(self)


class testclefs(testRun):

    def setUp(self):
        self.file = os.path.join(folder, "clefs.xml")
        parser = MxmlParser.MxmlParser()
        self.item = parser.parse(self.file)
        testRun.setUp(self)


class testdurationandstem(testRun):

    def setUp(self):
        self.file = os.path.join(folder, "duration_and_stem_direction.xml")
        parser = MxmlParser.MxmlParser()
        self.item = parser.parse(self.file)
        testRun.setUp(self)


class testdynamics(testRun):

    def setUp(self):
        self.file = os.path.join(folder, "dynamics.xml")
        parser = MxmlParser.MxmlParser()
        self.item = parser.parse(self.file)
        testRun.setUp(self)


class testfingering(testRun):

    def setUp(self):
        self.file = os.path.join(folder, "fingering.xml")
        parser = MxmlParser.MxmlParser()
        self.item = parser.parse(self.file)
        testRun.setUp(self)


class testgracenotes(testRun):

    def setUp(self):
        self.file = os.path.join(folder, "GraceNotes.xml")
        parser = MxmlParser.MxmlParser()
        self.item = parser.parse(self.file)
        self.dontcleanup = True
        testRun.setUp(self)


class testkeysig(testRun):

    def setUp(self):
        self.file = os.path.join(folder, "keySignatures.xml")
        parser = MxmlParser.MxmlParser()
        self.item = parser.parse(self.file)
        testRun.setUp(self)

# TODO: fix this, the problem is with alternative barlines
# class testlines(testRun):
#     def setUp(self):
#         self.file = os.path.join(folder, "lines.xml")
#         parser = MxmlParser.MxmlParser()
#         self.item = parser.parse(self.file)
#
#         self.dontcleanup = True
#         testRun.setUp(self)


class testmultiple(testRun):

    def setUp(self):
        self.file = os.path.join(folder, "multiple_parts.xml")
        parser = MxmlParser.MxmlParser()
        self.item = parser.parse(self.file)

        testRun.setUp(self)


class testnoteheads(testRun):

    def setUp(self):
        self.file = os.path.join(folder, "noteheads.xml")
        parser = MxmlParser.MxmlParser()
        self.item = parser.parse(self.file)
        testRun.setUp(self)


class testrepeats(testRun):

    def setUp(self):
        self.file = os.path.join(folder, "repeatMarks.xml")
        parser = MxmlParser.MxmlParser()
        self.item = parser.parse(self.file)
        self.dontcleanup = True
        testRun.setUp(self)


class testtext(testRun):

    def setUp(self):
        self.file = os.path.join(folder, "text.xml")
        parser = MxmlParser.MxmlParser()
        self.item = parser.parse(self.file)
        self.dontcleanup = True
        testRun.setUp(self)


class testtremolo(testRun):

    def setUp(self):
        self.file = os.path.join(folder, "Tremolo.xml")
        parser = MxmlParser.MxmlParser()
        self.item = parser.parse(self.file)
        self.dontcleanup = True
        testRun.setUp(self)


class testtrills(testRun):

    def setUp(self):
        self.file = os.path.join(folder, "TrillsFermataOrnaments.xml")
        parser = MxmlParser.MxmlParser()
        self.item = parser.parse(self.file)
        self.dontcleanup = True
        testRun.setUp(self)


class testtuplets(testRun):

    def setUp(self):
        self.file = os.path.join(folder, "tuplets.xml")
        parser = MxmlParser.MxmlParser()
        self.item = parser.parse(self.file)
        self.dontcleanup = True
        testRun.setUp(self)


class testtwostavesonepart(testRun):

    def setUp(self):
        self.file = os.path.join(folder, "two_staves_one_part.xml")
        parser = MxmlParser.MxmlParser()
        self.item = parser.parse(self.file)
        testRun.setUp(self)
