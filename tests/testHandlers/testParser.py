import unittest
from unittest import mock
from museparse import exceptions
from museparse.elements import part
from museparse.input import mxmlparser


class testSaxParser(unittest.TestCase):

    def setUp(self):
        self.parser = mxmlparser.MxmlParser()
        self.tag_list = []
        self.attrs = []

    # methods testing the startTag method in exclusion
    def test1Tag(self):
        tag = "score-partwise"
        self.parser.StartTag(tag, {})
        self.assertEqual(
            1, len(
                self.parser.tags), "ERROR: test1Tag failed because tag is not getting added to tag list")

    def test2Tags(self):
        tag = "score-partwise"
        tag2 = "movement-title"
        self.parser.StartTag(tag, {})
        self.parser.StartTag(tag2, {})
        self.assertEqual(
            2, len(
                self.parser.tags), "ERROR: test2Tags failed because both tags were not added to tag list")

    def testTagWithAttrs(self):
        tag = "wibble"
        attrs = {"tempo": 85}
        self.parser.StartTag(tag, attrs)
        self.assertEqual(
            attrs,
            self.parser.attribs["wibble"],
            "ERROR: TestTagWithAttrs failed because attribs doesn't match expected value")

    def testHandlerSet(self):
        self.assertEqual(
            None,
            self.parser.handler,
            "ERROR: TestHandlerSet failed - handler in parser should be none if StartTag not called")

    def testHandlerValue(self):
        tag = "movement-title"
        handler = mxmlparser.SetupPiece
        self.parser.StartTag(tag, None)
        self.assertEqual(
            handler,
            self.parser.handler,
            "ERROR: TestHandlerValue failed - handler should be SetupPiece when tag is movement-title")

    def testHandlerCall(self):
        tag = "type"
        self.parser.handler = mock.MagicMock()
        self.parser.EndTag(tag)
        self.parser.handler.assert_called_once_with(
            self.parser.tags, {}, {}, self.parser.piece, self.parser.data)

    # methods testing the newdata method
    def testCharsVal(self):
        self.assertEqual(
            0, len(
                self.parser.chars), "ERROR: testCharsVal failed as chars dict should be empty")

    def testTagInDict(self):
        tag = "whut"
        chars = "hello"
        self.parser.StartTag(tag, None)
        self.parser.NewData(chars)
        self.assertTrue(
            tag in self.parser.chars,
            "ERROR: testTagInDict failed as tag should be an index in chars dict")

    def testCharsInDict(self):
        chars = "hello"
        tag = "whaddup"
        self.parser.StartTag(tag, None)
        self.parser.NewData(chars)
        self.assertEqual(chars, self.parser.chars[tag])

    # methods testing the endtag method
    def testTagLength(self):
        tag = "hello"
        self.parser.StartTag(tag, {})
        self.assertEqual(1, len(self.parser.tags),
                         "ERROR: tag not being added in testTagLength")
        self.parser.EndTag(tag)
        self.assertEqual(0, len(self.parser.tags),
                         "ERROR: tag not being removed in testTagLength")

    def testCharsLength(self):
        tag = "hello"
        val = "world"
        self.parser.StartTag(tag, {})
        self.parser.NewData(val)
        self.assertTrue(tag in self.parser.chars.keys(),
                        "ERROR: data not being added in testCharsLength")
        self.parser.EndTag(tag)
        self.assertFalse(tag in self.parser.chars.keys(),
                         "ERROR: data not being removed in testCharsLength")

    def testAttrsLength(self):
        tag = "hello"
        val = "world"
        attrs = {"twist": "and shout"}
        self.parser.StartTag(tag, attrs)
        self.assertTrue(tag in self.parser.attribs.keys(),
                        "ERROR: attrs not being added in testAttrsLength")
        self.parser.EndTag(tag)
        self.assertFalse(tag in self.parser.attribs.keys(),
                         "ERROR: attrs not being removed in testAttrsLength")

    def testHandlerVal(self):
        tag = "movement-title"
        self.parser.StartTag(tag, {})
        handler = mxmlparser.SetupPiece
        self.assertEqual(
            handler,
            self.parser.handler,
            "ERROR: handler not set correctly in testHandlerVal")
        self.parser.EndTag(tag)
        self.assertEqual(
            None,
            self.parser.handler,
            "ERROR: handler not unset correctly in testHandlerVal")

    def testNoteGlobalVal(self):
        mxmlparser.note = "whaddup"
        self.parser.tags.append("note")
        self.parser.EndTag("note")
        self.assertEqual(
            None,
            self.parser.data["note"],
            "ERROR: note global val unset incorrectly in testNoteGlobalVal")

    def testHasPreviousHandler(self):
        self.parser.tags.append("measure")
        self.parser.tags.append("note")
        self.parser.EndTag("note")
        self.assertEqual(mxmlparser.HandleMeasures, self.parser.handler)


class testBackupAndForward(unittest.TestCase):

    def setUp(self):
        self.parser = mxmlparser.mxmlparser()
        self.tag_list = []
        self.attrs = []
        self.parser.piece.addPart(part.Part(), index="P1")
        self.parser.tags.append("part")
        self.parser.attribs["part"] = {"id": "P1"}
        self.parser.StartTag("measure", {"number": "1"})
        self.parser.StartTag("divisions", {})
        self.parser.NewData("8")
        self.parser.EndTag("divisions")
        self.parser.StartTag("note", {})
        self.parser.StartTag("duration", {})
        self.parser.NewData("16")
        self.parser.EndTag("duration")
        self.parser.EndTag("note")
        self.parser.StartTag("note", {})
        self.parser.StartTag("duration", {})
        self.parser.NewData("16")
        self.parser.EndTag("duration")
        self.parser.EndTag("note")
        self.parser.data["staff_id"] = 2
        self.parser.StartTag("note", {})
        self.parser.StartTag("divisions", {})
        self.parser.NewData("8")
        self.parser.EndTag("divisions")
        self.parser.StartTag("note", {})
        self.parser.StartTag("duration", {})
        self.parser.NewData("16")
        self.parser.EndTag("duration")
        self.parser.EndTag("note")
        self.parser.StartTag("note", {})
        self.parser.StartTag("duration", {})
        self.parser.NewData("16")
        self.parser.EndTag("duration")
        self.parser.EndTag("note")
        self.parser.data["staff_id"] = 1

        self.measure = self.parser.piece.getPart("P1").getMeasure(1, 1)

    def testBackupTag(self):
        self.assertEqual(self.measure.index, 2)
        self.parser.StartTag("backup", {})
        self.parser.StartTag("duration", {})
        self.parser.NewData("4")
        self.parser.EndTag("duration")
        self.assertEqual(self.measure.index, 1)

    def testForwardTag(self):
        self.assertEqual(self.measure.index, 2)
        self.parser.StartTag("forward", {})
        self.parser.StartTag("duration", {})
        self.parser.NewData("16")
        self.parser.EndTag("duration")
        self.assertEqual(self.measure.index, 3)

    def testBackupTagSecondStave(self):
        m = self.parser.piece.getPart("P1").getMeasure(1, 2)
        self.assertEqual(m.index, 2)
        self.parser.StartTag("backup", {})
        self.parser.StartTag("duration", {})
        self.parser.NewData("4")
        self.parser.EndTag("duration")
        self.assertEqual(m.index, 1)

    def testForwardTagSecondStave(self):
        m = self.parser.piece.getPart("P1").getMeasure(1, 2)
        self.assertEqual(m.index, 2)
        self.parser.StartTag("forward", {})
        self.parser.StartTag("duration", {})
        self.parser.NewData("16")
        self.parser.EndTag("duration")
        self.assertEqual(m.index, 3)

    def tearDown(self):
        self.parser.data["staff_id"] = 1


class testDrumAndGuitarTabHandling(unittest.TestCase):

    def setUp(self):
        self.parser = mxmlparser.mxmlparser()
        self.tag_list = []
        self.attrs = []

    def testGuitarTab(self):
        self.parser.StartTag("score-part", {"id": "P1"})
        self.parser.StartTag("part", {"id": "P1"})
        self.parser.StartTag("measure", {"number": "1"})
        self.parser.StartTag("clef", {})
        self.parser.StartTag("sign", {})
        self.parser.NewData("tab")
        self.parser.EndTag("sign")
        self.parser.EndTag("clef")
        self.parser.EndTag("measure")
        with self.assertRaises(exceptions.TabNotImplementedException):
            self.parser.EndTag("part")
        self.assertIsNone(self.parser.piece.getPart("P1"))

    def testDrumTab(self):
        self.parser.StartTag("score-part", {"id": "P1"})
        self.parser.StartTag("part", {"id": "P1"})
        self.parser.StartTag("measure", {"number": "1"})
        self.parser.StartTag("clef", {})
        self.parser.StartTag("sign", {})
        self.parser.NewData("percussion")
        self.parser.EndTag("sign")
        self.parser.EndTag("clef")
        self.parser.EndTag("measure")
        with self.assertRaises(exceptions.DrumNotImplementedException):
            self.parser.EndTag("part")
        self.assertIsNone(self.parser.piece.getPart("P1"))
