import unittest
import os
import sys
from os.path import expanduser
from museparse.classes.Output import LilypondOutput


class Lily(unittest.TestCase):

    def setUp(self):
        self.compile = False
        self.wrappers = []

    def testValue(self):
        if hasattr(self, "lilystring"):
            if hasattr(self, "item"):
                self.assertEqual(self.lilystring, self.item.to_lily())

    def testCompilation(self):
        if hasattr(self, "compile") and self.compile is True:

            filepath = expanduser("~")
            script = ''
            if sys.platform == 'darwin':
                script = os.path.join(filepath, 'bin', 'lilypond')
            filepath = os.path.join(filepath, self.name)
            if self.compile and hasattr(self, "item"):
                if os.path.exists(filepath + ".pdf"):
                    os.remove(filepath + ".pdf")

                ly = LilypondOutput.LilypondRenderer(
                    self.item, filepath + ".xml", script)
                if hasattr(self, "wrappers"):
                    ly.run(wrappers=self.wrappers)
                else:
                    ly.run()
                self.assertTrue(os.path.exists(filepath + ".pdf"))
