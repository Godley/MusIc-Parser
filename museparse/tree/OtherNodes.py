from museparse.classes.ObjectHierarchy.TreeClasses.BaseTree import Node

"""these nodes are generally standalone, hence the grouping"""


class SelfNode(Node):

    def __init__(self):
        Node.__init__(self, rules=[type(self)], limit=1)

    def toLily(self):
        '''

        Method which converts the object instance and its attributes to a string of lilypond code

        :return: str of lilypond code
        '''
        lilystring = ""
        if self.item is not None:
            lstring = self.item.to_lily()
            if isinstance(lstring, str):
                lilystring += lstring
            else:
                lilystring = lstring
        child = self.GetChild(0)
        if child is not None:
            if isinstance(lilystring, str):
                lilystring += child.to_lily()
            else:
                lilystring.append(child.to_lily())
        return lilystring


class DirectionNode(SelfNode):
    pass


class ExpressionNode(SelfNode):
    pass


class KeyNode(Node):

    def __init__(self):
        Node.__init__(self, limit=-1)

    def toLily(self):
        lstring = ""
        if self.item is not None:
            lstring += self.item.to_lily()
        return lstring


class ClefNode(KeyNode):
    pass
