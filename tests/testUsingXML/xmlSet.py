import unittest

from museparse.classes.Input import MxmlParser


def parsePiece(name):
    parser = MxmlParser.MxmlParser()
    return parser.parse(name)


class xmlSet(unittest.TestCase):

    def setUp(self):
        self.fname = ""
        self.note_num = 0
        self.parser = MxmlParser.MxmlParser()
        self.folder = "/Users/charlottegodley/PycharmProjects/FYP/implementation/primaries/SampleMusicXML/testcases"
