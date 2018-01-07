import unittest

from museparse.input import mxmlparser
from museparse.tree.piecetree import PieceTree


class testSetupPiece(unittest.TestCase):

    def setUp(self):
        self.handler = mxmlparser.SetupPiece
        self.tags = []
        self.attrs = {}
        self.chars = {}
        self.data = {}
        self.piece = PieceTree()

    def testNoTags(self):
        self.assertEqual(
            None,
            self.handler(
                self.tags,
                self.attrs,
                self.chars,
                self.piece,
                self.data),
            "ERROR: testNoTags failed: nothing should happen if there are no tags in list")

    def testMetaExists(self):
        self.assertFalse(
            hasattr(
                self.piece.GetItem(),
                "meta"),
            "ERROR: testMetaExists failed: meta should not be set in piece class at beginning of testing")

    def testIrrelevantTag(self):
        self.tags.append("lol")
        self.assertEqual(
            None,
            self.handler(
                self.tags,
                self.attrs,
                self.chars,
                self.piece,
                self.data),
            "ERROR: irrelevant tag should do nothing in TestIrrelevance")

    def testTitleTag(self):
        self.tags.append("movement-title")
        self.chars["movement-title"] = "hehehe"
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)
        self.assertTrue(hasattr(self.piece.GetItem(), "meta"),
                        "ERROR: Meta should exist in TestTitleTag")
        self.assertEqual(
            "hehehe",
            self.piece.GetItem().meta.title,
            "ERROR: title set incorrectly in TestTitleTag")

    def testRightsTag(self):
        self.tags.append("rights")
        self.chars["rights"] = "lee"
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)
        self.assertTrue(hasattr(self.piece.GetItem(), "meta"))
        self.assertEqual("lee ", self.piece.GetItem().meta.copyright)

    def testCompTag(self):
        self.tags.append("creator")
        self.attrs["creator"] = {"type": "composer"}
        self.chars["creator"] = "lee"

        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)
        self.assertTrue(
            hasattr(
                self.piece.GetItem(),
                "meta"),
            "ERROR: meta should exist in piece class in TestCompTag")
        self.assertEqual(
            "lee",
            self.piece.GetItem().meta.composer,
            "ERROR: composer should match expected in TestCompTag")

    def testTitleCompTag(self):
        self.tags.append("creator")
        self.attrs["creator"] = {"type": "composer"}
        self.chars["creator"] = "lee"
        self.chars["movement-title"] = "hello world"
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)
        self.assertTrue(
            hasattr(
                self.piece.GetItem().meta,
                "composer"),
            "ERROR: meta should have composer attrib in TestTitleCompTag")
        self.assertEqual(
            "lee",
            self.piece.GetItem().meta.composer,
            "ERROR: composer should match test in TestTitleCompTag")
        self.tags.append("movement-title")
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)
        self.assertTrue(
            hasattr(
                self.piece.GetItem().meta,
                "title"),
            "ERROR: meta should have title in TestTitleCompTag")
        self.assertEqual(
            "hello world",
            self.piece.GetItem().meta.title,
            "ERROR: meta title set incorrectly in TestTitleCompTag")


class testHandlePart(unittest.TestCase):

    def setUp(self):
        self.handler = mxmlparser.UpdatePart
        self.tags = []
        self.chars = {}
        self.attrs = {}
        self.piece = PieceTree()
        self.data = {}

    def testNoData(self):
        self.assertEqual(
            None,
            self.handler(
                self.tags,
                self.attrs,
                self.chars,
                self.piece,
                self.data),
            "ERROR: no tags should return none in TestNodata")

    def testIrrelevantTag(self):
        self.tags.append("wut")
        mxmlparser.part_id = None
        self.assertEqual(
            None,
            self.handler(
                self.tags,
                self.attrs,
                self.chars,
                self.piece,
                self.data),
            "ERROR: irrelevant tags should return none in TestIrrelevantTag")

    def testScorePartTag(self):
        mxmlparser.part_id = None
        self.assertEqual(
            None,
            mxmlparser.part_id,
            "ERROR: part_id not none in testScorePartTag")
        self.tags.append("score-part")
        self.attrs["score-part"] = {"id": "P1"}
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)
        self.assertEqual(1, len(self.piece.root.GetChildrenIndexes()))

    def testPnameTag(self):
        self.assertEqual(0, len(self.piece.root.GetChildrenIndexes()))
        self.tags.append("score-part")
        self.attrs["score-part"] = {"id": "P1"}
        self.tags.append("part-name")
        self.chars["part-name"] = "will"
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)
        self.assertEqual("will", self.piece.getPart("P1").GetItem().name)

    def testPNameWithShortName(self):
        self.assertEqual(0, len(self.piece.root.GetChildrenIndexes()))
        self.tags.append("score-part")
        self.attrs["score-part"] = {"id": "P1"}
        self.tags.append("part-abbreviation")
        self.chars["part-abbreviation"] = "w"
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)
        self.assertEqual("w", self.piece.getPart("P1").GetItem().shortname)

    def testPartGroupOpen(self):
        self.tags.append("part-group")
        self.attrs["part-group"] = {"number": "1", "type": "start"}
        self.tags.append("score-part")
        self.attrs["score-part"] = {"id": "P1"}
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)
        self.tags.append("score-part")
        self.attrs["score-part"] = {"id": "P2"}
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)
        self.assertEqual(["P1", "P2"], self.piece.getGroup(1))

    def testPartGroupClose(self):
        self.tags.append("part-group")
        self.attrs["part-group"] = {"number": "1", "type": "start"}
        self.tags.append("score-part")
        self.attrs["score-part"] = {"id": "P1"}
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)
        self.tags.append("part-group")
        self.attrs["part-group"] = {"number": "1", "type": "stop"}
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)
        self.tags.append("score-part")
        self.attrs["score-part"] = {"id": "P2"}
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)
        self.assertEqual(["P1"], self.piece.getGroup(1))


class testRights(unittest.TestCase):

    def setUp(self):
        testSetupPiece.setUp(self)
        self.data = {}
        self.tags.append("credit")
        self.tags.append("credit-type")
        self.chars["credit-type"] = "rights"
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)

    def testRightsCredit(self):
        self.tags.append("credit-words")
        self.chars["credit-words"] = "copyright lol"
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)
        self.assertTrue(hasattr(self.piece.GetItem().meta, "copyright"))

    def testRightsValue(self):
        self.tags.append("credit-words")
        self.chars["credit-words"] = "copyright lol"
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)
        self.assertEqual(self.piece.GetItem().meta.copyright, "copyright lol")
