import unittest
import os
import sys
import subprocess
from museparse.output.helpers import setupLilypondClean as setupLilypond


class testLilySetup(unittest.TestCase):

    def setUp(self):
        pass

    def testSetup(self):
        path = ''
        if sys.platform != 'win32':
            path = '~/bin'
        else:
            path = 'C:/Program Files (x86)/LilyPond/usr/bin'
        setupLilypond(path)
        batcmd = 'lilypond'

        output = subprocess.Popen(
            ["lilypond"],
            stderr=subprocess.PIPE,
            shell=True).communicate()[0]
        self.assertIsNone(output)
