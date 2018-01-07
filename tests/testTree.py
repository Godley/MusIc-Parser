import unittest

from museparse.tree import basetree


class testTree(unittest.TestCase):

    def setUp(self):
        self.item = basetree.Tree()

    def testAddNode(self):
        elem = basetree.Node()
        self.item.AddNode(elem)
        self.assertEqual(elem, self.item.root)

    def testAddInvalidNode(self):
        elem = basetree.Node()
        self.item.AddNode(elem)
        self.assertRaises(
            basetree.CannotAddToTreeException,
            self.item.AddNode,
            basetree.Node())

    def testAddTwoValidNodes(self):
        elem = basetree.Node(rules=[basetree.EmptyNode, basetree.IndexedNode])
        self.item.AddNode(elem)
        self.item.AddNode(basetree.EmptyNode(0))
        self.assertEqual(1, len(elem.children))

    def testAddNodeOverLimit(self):
        elem = basetree.Node(
            rules=[
                basetree.EmptyNode,
                basetree.IndexedNode],
            limit=-1)
        self.item.AddNode(elem)
        self.assertRaises(
            basetree.CannotAddToTreeException,
            self.item.AddNode,
            basetree.EmptyNode(0))

    def testAddNodeAddsToNextLevel(self):
        # this test confirms that with a parent who allows 1 child which has to be empty or indexed, Next is it's child
        # and third is a child of next.
        elem = basetree.Node(
            rules=[
                basetree.EmptyNode,
                basetree.IndexedNode],
            limit=1)
        next = basetree.EmptyNode(0, rules=[basetree.Node])
        third = basetree.Node()
        self.item.AddNode(elem)
        self.item.AddNode(next)
        self.item.AddNode(third)
        self.assertEqual(next.GetChild(0), third)

    def testAddNodeAddsToNextLevelWithExpandedLimit(self):
        # this test confirms the above still happens when the limit is 2
        elem = basetree.Node(
            rules=[
                basetree.EmptyNode,
                basetree.IndexedNode],
            limit=2)
        next = basetree.EmptyNode(0, rules=[basetree.Node])
        third = basetree.Node()
        self.item.AddNode(elem)
        self.item.AddNode(next)
        self.item.AddNode(third)
        self.assertEqual(next.GetChild(0), third)

    def testAddNodeAddsToCurrentLevelWithRelevantRuleAndLimit(self):
        # this test confirms the first spot for third to land in is a second child of elem, because elem lets you have
        # node as a child and can have 2 children.
        elem = basetree.Node(
            rules=[
                basetree.EmptyNode,
                basetree.Node],
            limit=2)
        next = basetree.EmptyNode(0, rules=[basetree.Node])
        third = basetree.Node()
        self.item.AddNode(elem)
        self.item.AddNode(next)
        self.item.AddNode(third)
        self.assertEqual(elem.GetChild(1), third)

    def testAddNodeWithIndex(self):
        elem = basetree.IndexedNode(rules=[basetree.EmptyNode], limit=1)
        second_elem = basetree.EmptyNode(0)
        self.item.AddNode(elem)
        self.item.AddNode(second_elem, index=2)
        self.assertEqual(elem.GetChild(2), second_elem)

    def testAddNodeToSecondNode(self):
        elem = basetree.Node(rules=[basetree.EmptyNode])
        self.item.AddNode(elem)
        second = basetree.EmptyNode(0)
        self.item.AddNode(second)
        third = basetree.EmptyNode(0, rules=[basetree.Node])
        self.item.AddNode(third)
        fourth = basetree.Node()
        self.item.AddNode(fourth)
        self.assertEqual(third.GetChild(0), fourth)

    def testAddNodeToThirdNode(self):
        elem = basetree.Node(rules=[basetree.EmptyNode])
        self.item.AddNode(elem)
        second = basetree.EmptyNode(0)
        self.item.AddNode(second)
        third = basetree.EmptyNode(0)
        self.item.AddNode(third)
        fourth = basetree.EmptyNode(0, rules=[basetree.Node])
        self.item.AddNode(fourth)
        fifth = basetree.Node()
        self.item.AddNode(fifth)
        self.assertEqual(fourth.GetChild(0), fifth)

    def testFindFirstNode(self):
        elem = basetree.Node()
        self.item.AddNode(elem)
        self.assertEqual(self.item.FindNode(type(elem), 1), elem)

    def testFindSecondNode(self):
        elem = basetree.Node(rules=[basetree.Node])
        self.item.AddNode(elem)
        second = basetree.Node()
        self.item.AddNode(second)
        node = self.item.FindNode(type(elem), 2)
        self.assertEqual(node, second)

    def testFindFirstEmptyNodeOnFirstChild(self):
        elem = basetree.Node(rules=[basetree.Node])
        self.item.AddNode(elem)
        second = basetree.Node(rules=[basetree.EmptyNode])
        self.item.AddNode(second)
        third = basetree.EmptyNode(0)
        self.item.AddNode(third)
        node = self.item.FindNode(basetree.EmptyNode, 1)
        self.assertEqual(node, third)

    def testFindEmptyNodeOnSecondChild(self):
        elem = basetree.Node(rules=[basetree.Node])
        self.item.AddNode(elem)
        second = basetree.Node()
        self.item.AddNode(second)
        third = basetree.Node(rules=[basetree.EmptyNode])
        self.item.AddNode(third)
        fourth = basetree.EmptyNode(0)
        self.item.AddNode(fourth)
        node = self.item.FindNode(basetree.EmptyNode, 1)
        self.assertEqual(node, fourth)

    def testFailure(self):
        elem = basetree.Node(rules=[basetree.Node])
        self.item.AddNode(elem)
        second = basetree.Node()
        self.item.AddNode(second)
        third = basetree.Node(rules=[basetree.EmptyNode])
        self.item.AddNode(third)
        with self.assertRaises(basetree.CannotFindInTreeException):
            self.item.FindNode(basetree.EmptyNode, 1)

    def testAddNodeWithStringIndex(self):
        elem = basetree.IndexedNode(rules=[basetree.Node])
        self.item.AddNode(elem)
        second = basetree.Node()
        self.item.AddNode(second, "P1")
        self.assertEqual(elem.GetChild("P1"), second)

    def testFindNodeWithStringIndex(self):
        elem = basetree.IndexedNode(rules=[basetree.Node])
        self.item.AddNode(elem)
        second = basetree.Node()
        self.item.AddNode(second, "P1")
        self.assertEqual(self.item.FindNodeByIndex("P1"), second)

    def testFindNodeWithStringIndexOnSecondLevel(self):
        elem = basetree.Node(rules=[basetree.IndexedNode])
        self.item.AddNode(elem)
        second = basetree.IndexedNode(rules=[basetree.Node])
        self.item.AddNode(second)
        third = basetree.Node()
        self.item.AddNode(third, "S")
        self.assertEqual(self.item.FindNodeByIndex("S"), third)

    def testFindNodeWithStringIndexOnSecondLevelWhereFirstLevelIsIndexed(self):
        elem = basetree.IndexedNode(rules=[basetree.IndexedNode])
        self.item.AddNode(elem)
        second = basetree.IndexedNode(rules=[basetree.Node])
        self.item.AddNode(second, "A")
        third = basetree.Node()
        self.item.AddNode(third, "B")
        self.assertEqual(self.item.FindNodeByIndex("B"), third)
