import unittest

from museparse.input import mxmlparser


class testCheckDynamics(unittest.TestCase):

    def setUp(self):
        self.handler = mxmlparser.CheckDynamics

    def testEmpty(self):
        self.assertFalse(self.handler(''))

    def testRandChar(self):
        self.assertFalse(self.handler('q'))

    def testP(self):
        self.assertTrue(self.handler('p'))

    def testF(self):
        self.assertTrue(self.handler('f'))

    def testmf(self):
        self.assertTrue(self.handler('mf'))

    def testmp(self):
        self.assertTrue(self.handler('mp'))

    def testpp(self):
        self.assertTrue(self.handler('pp'))

    def testff(self):
        self.assertTrue(self.handler('ff'))

    def testm(self):
        self.assertFalse(self.handler('m'))

    def testfm(self):
        self.assertFalse(self.handler('fm'))

    def testpm(self):
        self.assertFalse(self.handler('pm'))

    def testmm(self):
        self.assertFalse(self.handler('mm'))
