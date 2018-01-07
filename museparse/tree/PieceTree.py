

from museparse.classes.ObjectHierarchy.TreeClasses import PartNode
from museparse.classes.ObjectHierarchy.TreeClasses.BaseTree import Tree, IndexedNode
from museparse.classes.ObjectHierarchy.ItemClasses import Piece


# \markup {
#     \column { "Clarinetti"
#       \line { "in B" \smaller \flat }
#     }
#   }

class PieceTree(Tree):

    def __init__(self):
        Tree.__init__(self)
        self.root = IndexedNode(rules=[PartNode.PartNode])
        self.item = Piece.Piece()
        self.groups = {}
        self.current = []

    def GetSortedChildren(self):
        children = self.root.GetChildrenIndexes()
        numbers = []
        for child in children:
            if child[0] == "P":
                number = child[1:len(child)]
                numbers.append(int(number))
        numbers.sort()
        part_ids = map(lambda x: "P" + str(x), numbers)
        return part_ids

    def SetValue(self, item):
        self.root.SetItem(item)

    def getLastPart(self):
        indexes = self.root.GetChildrenIndexes()
        if len(indexes) > 0:
            return self.getPart(indexes[-1])

    def addPart(self, item, index=-1):
        node = PartNode.PartNode(index=index)
        node.SetItem(item)
        self.AddNode(node, index=index)
        if len(self.current) > 0:
            for item in self.current:
                self.AddToGroup(item, index)

    def removePart(self, id):
        if id in self.root.children:
            self.root.PopChild(id)

    def startGroup(self, index):
        if index not in self.groups:
            self.groups[index] = []
        if index not in self.current:
            self.current.append(index)

    def stopGroup(self, index):
        if index in self.current:
            self.current.remove(index)

    def AddToGroup(self, name, index):
        if name not in self.groups:
            self.groups[name] = []
        if isinstance(index, str) and index not in self.groups[name]:
            self.groups[name].append(index)
        elif isinstance(index, list):
            self.groups[name].append(index)

    def getGroup(self, name):
        if name in self.groups:
            return self.groups[name]

    def getPart(self, key):
        return self.FindNodeByIndex(key)

    def GetItem(self):
        return self.item

    def SetItem(self, i):
        self.item = i

    def handleGroups(self):
        lilystring = ""
        ids_loaded = []
        groupings = []
        group_ids = sorted(
            self.groups,
            key=lambda k: len(
                self.groups[k]),
            reverse=True)
        for i in range(len(group_ids)):
            merger = []
            for j in range(i + 1, len(group_ids)):
                for k in self.groups[group_ids[j]]:
                    if k in self.groups[group_ids[i]]:
                        merger.append(k)
            if len(merger) > 0:
                for group in group_ids:
                    [self.groups[group].remove(
                        a) for a in self.groups[group] if a in merger]
                self.AddToGroup(group_ids[i], merger)
        for group in group_ids:
            groupstr = "\\new StaffGroup <<"
            not_nested = sorted(
                [g for g in self.groups[group] if not isinstance(g, list)])
            not_nested.extend(
                [g for g in self.groups[group] if isinstance(g, list)])
            for element in not_nested:
                if not isinstance(element, list) and element not in ids_loaded:
                    part = self.getPart(element)
                    pstring = part.to_lily()
                    lilystring += pstring[0]
                    groupstr += pstring[1]
                    ids_loaded.append(element)
                elif isinstance(element, list):
                    groupstr += "\\new StaffGroup <<"
                    for nested_part in element:
                        part = self.getPart(nested_part)
                        pstring = part.to_lily()
                        lilystring += pstring[0]
                        groupstr += pstring[1]
                        ids_loaded.append(nested_part)
                    groupstr += ">>"
            groupstr += ">>"
            groupings.append(groupstr)
        return lilystring, groupings, ids_loaded

    def toLily(self):
        '''
        Method which converts the object instance, its attributes and children to a string of lilypond code

        :return: str of lilypond code
        '''
        lilystring = "\\version \"2.18.2\" \n"

        partstrings = []
        ids_loaded = []
        groupings = []
        if len(self.groups) > 0:
            # here we need to do some set union theory
            lstring, groupings, ids_loaded = self.handleGroups()
            lilystring += lstring
        children = [
            child for child in self.GetSortedChildren() if child not in ids_loaded]
        for child in children:
            part = self.getPart(child)
            partstring = part.to_lily()
            lilystring += partstring[0]
            partstrings.append(partstring[1])
        lilystring += self.item.to_lily()
        lilystring += "<<"
        lilystring += "".join([gstring for gstring in groupings])
        lilystring += "".join([partstring for partstring in partstrings])
        lilystring += ">>"
        return lilystring
