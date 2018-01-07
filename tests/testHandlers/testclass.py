import unittest

from museparse.tree.piecetree import PieceTree


class TestClass(unittest.TestCase):

    def setUp(self):
        self.tags = []
        self.attrs = {}
        self.chars = {}
        self.piece = PieceTree()
