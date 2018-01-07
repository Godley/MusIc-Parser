import copy

from museparse.classes.ObjectHierarchy.TreeClasses.BaseTree import Node, FindPosition
from museparse.classes.ObjectHierarchy.TreeClasses import OtherNodes
from museparse.classes.ObjectHierarchy.ItemClasses.Directions import OctaveShift
from museparse.classes.ObjectHierarchy.ItemClasses.Note import Arpeggiate, NonArpeggiate, \
    GraceNote
from museparse.classes.ObjectHierarchy.ItemClasses import Note
from museparse.classes.ObjectHierarchy.TreeClasses.OtherNodes import ExpressionNode


class NoteNode(Node):

    """Node which encapsulates the Note class.


    Optional inputs are minimal on this one as info about the note itself is stored in the Note class.


    In order to maintain lilypond's output flow, Notes have a specific child order:

        - left: Expression (dynamic or other expressive thing that has to be attached to a note)

        - middle: Any other notes, if this note is part of a chord

        - right: direction (anything that's not a note or expression)"""

    def __init__(self, **kwargs):
        if "duration" in kwargs:
            self.duration = kwargs["duration"]
        Node.__init__(
            self,
            rules=[
                OtherNodes.DirectionNode,
                OtherNodes.ExpressionNode,
                NoteNode],
            limit=3)
        if self.item is None:
            self.item = Note.Note()

    def Find(self, node_type, item_type):
        '''
        method for finding specific types of notation from nodes.
        will currently return the first one it encounters because this method's only really intended
        for some types of notation for which the exact value doesn't really
        matter.


        :param node_type: the type of node to look under

        :param item_type: the type of item (notation) being searched for

        :return: first item_type object encountered
        '''

        if node_type == OtherNodes.DirectionNode:
            child = self.GetChild(len(self.children) - 1)
            while child is not None and not isinstance(
                    child.GetItem(),
                    item_type):
                if child.GetItem().__class__.__name__ == item_type.__name__:
                    return True
                child = child.GetChild(0)
        if node_type == OtherNodes.ExpressionNode:
            child = self.GetChild(len(self.children) - 2)
            while child is not None and not isinstance(
                    child.GetItem(),
                    item_type):
                if child.GetItem().__class__.__name__ == item_type.__name__:
                    return True
                child = child.GetChild(0)

    def SetGrace(self):
        if self.item.search(GraceNote) is None:
            self.item.add_notation(GraceNote())

    def SetLast(self):
        result = self.item.search(GraceNote)
        if result is not None:
            result.last = True

    def UpdateArpeggiates(self, type="start"):
        '''
        method which searches for all arpeggiates and updates the top one of each chord to be a start,
        and the bottom one to be a stop ready for lilypond output
        :param type:
        :return:
        '''
        result = self.item.search(Arpeggiate)
        if result is not None:
            if type == "start":
                result.type = type
            child = self.GetChild(0)
            if child is not None:
                if child.item.search(Arpeggiate) is None:
                    new_obj = copy.deepcopy(result)
                    new_obj.type = "none"
                    child.GetItem().add_notation(new_obj)
                if child is not None and hasattr(child, "UpdateArpeggiates"):
                    child.UpdateArpeggiates(type="stop")
            else:
                result.type = type
        else:
            result = self.item.search(NonArpeggiate)
            if result is not None:
                if type == "start":
                    result.type = type
                child = self.GetChild(0)
                if child is not None:
                    search = child.item.search(NonArpeggiate)
                    if search is None:
                        cpy = copy.deepcopy(result)
                        cpy.type = "none"
                        child.item.add_notation(cpy)
                    if hasattr(child, "UpdateArpeggiates"):
                        child.UpdateArpeggiates(type="bottom")
                else:
                    result.type = type

    def SetItem(self, new_item):
        Node.SetItem(self, new_item)
        if hasattr(new_item, "duration"):
            self.duration = new_item.duration
        else:
            self.duration = 0

    def CheckForGraceNotes(self):
        result = self.item.search(GraceNote)
        if result is not None:
            first_child = self.GetChild(0)
            if isinstance(self.GetChild(0), NoteNode):
                first_child.SetGrace()
                first_child.CheckForGraceNotes()
            else:
                self.SetLast()

    def AttachDirection(self, item):
        if item.GetItem().__class__.__name__ == OctaveShift.__name__:
            self.shift = True
        if len(self.children) == 0:
            self.AttachExpression(OtherNodes.ExpressionNode())
            self.AddChild(item)
        elif 3 > len(self.children) > 0:
            if not isinstance(self.GetChild(0), NoteNode):
                if not isinstance(self.GetChild(0), OtherNodes.ExpressionNode):
                    self.AttachExpression(OtherNodes.ExpressionNode())
                dir = self.GetChild(1)
                if isinstance(dir, OtherNodes.DirectionNode):
                    parent = FindPosition(dir, item)
                    if parent is not None:
                        parent.AddChild(item)
                elif dir is None:
                    self.AddChild(item)
            elif not isinstance(self.GetChild(1), ExpressionNode):
                self.AttachExpression(ExpressionNode())
                self.AddChild(item)
        else:
            dir_node = self.GetChild(len(self.children) - 1)
            if dir_node is not None:
                if dir_node.GetItem() is None:
                    dir_node.SetItem(item.GetItem())
                else:
                    parent = FindPosition(dir_node, item)
                    if parent is not None:
                        parent.AddChild(item)
            else:
                self.AddChild(item)

    def AttachExpression(self, new_node):
        if len(self.children) > 0:
            if isinstance(self.GetChild(0), OtherNodes.DirectionNode):
                self.PositionChild(0, new_node)
            if isinstance(self.GetChild(0), NoteNode):
                second = self.GetChild(1)
                if second is None:
                    self.AddChild(new_node)
                elif isinstance(second, OtherNodes.ExpressionNode):
                    node = FindPosition(second, new_node)
                    node.AddChild(new_node)
                else:
                    self.PositionChild(1, new_node)
            elif isinstance(self.GetChild(0), OtherNodes.ExpressionNode):
                parent = self.GetChild(0)
                node = FindPosition(parent, new_node)
                node.AddChild(new_node)
        else:
            self.AddChild(new_node)

    def AttachNote(self, new_note):

        if len(self.children) > 0:
            firstchild = self.GetChild(0)
            if isinstance(firstchild, NoteNode):
                firstchild.AttachNote(new_note)
            else:
                if not isinstance(
                        new_note.GetItem(),
                        int) and not isinstance(
                        new_note.GetItem(),
                        str):
                    post, pre, wrap = new_note.GetItem().get_all_notation()
                    [self.GetItem().add_notation(n)
                     for n in post if self.GetItem().search(type(n)) is None]
                    [self.GetItem().add_notation(p)
                     for p in pre if self.GetItem().search(type(p)) is None]
                    [self.GetItem().add_notation(w)
                     for w in wrap if self.GetItem().search(type(w)) is None]
                    new_note.GetItem().flush_notation()
                self.PositionChild(0, new_note)
        else:
            if not isinstance(
                    new_note.GetItem(),
                    int) and not isinstance(
                    new_note.GetItem(),
                    str):
                post, pre, wrap = new_note.GetItem().get_all_notation()
                [self.GetItem().add_notation(n)
                 for n in post if self.GetItem().search(type(n)) is None]
                [self.GetItem().add_notation(p)
                 for p in pre if self.GetItem().search(type(p)) is None]
                [self.GetItem().add_notation(w)
                 for w in wrap if self.GetItem().search(type(w)) is None]
                new_note.GetItem().flush_notation()
            self.AddChild(new_note)

    def toLily(self):
        '''
        Method which converts the object instance, its attributes and children to a string of lilypond code

        :return: str of lilypond code
        '''
        lilystring = ""
        if self.item is not None:
            if not isinstance(self.GetChild(0), NoteNode):
                if hasattr(self.item, "chord") and self.item.chord:
                    self.item.chord = "stop"
            if isinstance(self.GetChild(0), NoteNode):
                if not hasattr(self.item, "chord") or not self.item.chord:
                    self.item.chord = "start"
            lilystring += self.item.to_lily()
        children = self.GetChildrenIndexes()
        written = False
        for child in children:
            if self.GetChild(child) is not None:
                if isinstance(self.GetChild(child), NoteNode):
                    lilystring += " "
                return_val = self.GetChild(child).to_lily()
                if isinstance(return_val, str):
                    lilystring += return_val
                else:
                    lilystring = return_val[0] + lilystring + return_val[1]
                if isinstance(child, OtherNodes.ExpressionNode):
                    written = True
                    lilystring += self.item.get_closing_notation_as_lilypond()

        if len(children) == 0 or not written:
            lilystring += self.item.get_closing_notation_as_lilypond()
        return lilystring

    def PositionChild(self, key, node):
        children = self.GetChildrenIndexes()
        if key in children:
            start = key
            popped = self.children[start:]
            self.children = self.children[:start]
            self.AddChild(node)
            [self.AddChild(pop) for pop in popped]


class Placeholder(NoteNode):

    def __init__(self, **kwargs):
        NoteNode.__init__(self, **kwargs)
        self.item = None

    def toLily(self):
        '''
        Method which converts the object instance, its attributes and children to a string of lilypond code

        :return: str of lilypond code
        '''
        lilystring = ""
        if self.duration > 0:
            lilystring += "r" + str(self.duration)
        return lilystring
