from tests.testHandlers import testclass
from museparse.elements import directions, part
from museparse.input import mxmlparser


class testRepeatSymbols(testclass.TestClass):

    def setUp(self):
        testclass.TestClass.setUp(self)
        self.handler = mxmlparser.HandleRepeatMarking
        self.piece.addPart(part.Part(), "P1")
        self.piece.getPart("P1").addEmptyMeasure(1, 1)
        self.attrs["measure"] = {"number": "1"}
        self.attrs["part"] = {"id": "P1"}
        self.measure = self.piece.getPart("P1").getMeasure(1, 1)
        self.tags.append("direction")
        self.attrs["direction"] = {"placement": "above"}
        self.data = {"staff_id": 1}

    def testSegno(self):
        self.tags.append("direction-type")
        self.tags.append("segno")
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)

        self.assertIsInstance(self.data["direction"], directions.RepeatSign)

    def testRType(self):
        self.tags.append("direction-type")
        self.tags.append("segno")
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)

        self.assertEqual("segno", self.data["direction"].type)

    def testCoda(self):
        self.tags.append("direction-type")
        self.tags.append("coda")
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)

        self.assertIsInstance(self.data["direction"], directions.RepeatSign)

    def testCType(self):
        self.tags.append("direction-type")
        self.tags.append("coda")
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)

        self.assertEqual("coda", self.data["direction"].type)

    def testSoundSegno(self):
        self.tags.append("sound")
        self.attrs["sound"] = {"segno": "segno"}
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)
        self.assertTrue(hasattr(self.measure, "segno"))
        self.assertEqual("segno", self.measure.segno)

    def testSoundCoda(self):
        self.tags.append("sound")
        self.attrs["sound"] = {"coda": "coda"}
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)
        self.assertTrue(hasattr(self.measure, "coda"))
        self.assertEqual("coda", self.measure.coda)

    def testSoundFine(self):
        self.tags.append("sound")
        self.attrs["sound"] = {"fine": "yes"}
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)
        self.assertTrue(hasattr(self.measure, "fine"))
        self.assertEqual(True, self.measure.fine)

    def testSoundDaCapo(self):
        self.tags.append("sound")
        self.attrs["sound"] = {"dacapo": "yes"}
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)
        self.assertTrue(hasattr(self.measure, "dacapo"))
        self.assertEqual(True, self.measure.dacapo)

    def testSoundDalSegno(self):
        self.tags.append("sound")
        self.attrs["sound"] = {"dalsegno": "segno"}
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)
        self.assertTrue(hasattr(self.measure, "dalsegno"))
        self.assertEqual("segno", self.measure.dalsegno)

    def testSoundToCoda(self):
        self.tags.append("sound")
        self.attrs["sound"] = {"tocoda": "coda"}
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)
        self.assertTrue(hasattr(self.measure, "tocoda"))
        self.assertEqual("coda", self.measure.tocoda)
