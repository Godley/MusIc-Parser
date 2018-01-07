

class CannotAddToTreeException(BaseException):

    '''error in tree addition!'''


class CannotFindInTreeException(BaseException):

    '''error! can't find element'''


def BackwardSearch(cls_type, node, index, depth=0, start_index=0):
    '''
    Helper method which backwards-recursively searches for objects
    :param cls_type: class type of the object we are in search of
    :param node: object instance to start at
    :param index: number of the object to look for e.g <cls_type> num 1
    :param depth: current depth in the tree
    :param start_index: index to start with in children
    :return: object <index> of <cls_type>
    '''
    counter = depth
    if isinstance(node, cls_type):
        counter += 1
        if counter == index:
            return node
    if node is None:
        return None
    else:
        children = node.GetChildrenIndexes()
        if len(children) == 0 and isinstance(node, cls_type):
            return counter
        else:
            children.reverse()
            for child in children:
                result = Search(
                    cls_type,
                    node.GetChild(child),
                    index,
                    depth=counter)
                if isinstance(result, int):
                    counter = result
                    if counter == index:
                        return node.GetChild(child)
                if isinstance(result, cls_type):
                    return result
            if isinstance(node, cls_type):
                if counter == index:
                    return node
                else:
                    return counter


def Search(cls_type, node, index, depth=0, start_index=0):
    '''
    recursive method that goes through finding the "index"th object of cls_type. outside of piecetree
    so that it can be used by any node
    :param cls_type: class type of the object we are in search of
    :param node: object instance to start at
    :param index: number of the object to look for e.g <cls_type> num 1
    :param depth: current depth in the tree
    :param start_index: index to start with in children
    :return: object <index> of <cls_type>
    '''
    counter = depth
    if isinstance(node, cls_type):
        counter += 1
        if counter == index:
            return node
    if node is None:
        return None
    else:
        children = node.GetChildrenIndexes()
        if len(children) == 0 and isinstance(node, cls_type):
            return counter
        else:
            for child in children:
                result = Search(
                    cls_type,
                    node.GetChild(child),
                    index,
                    depth=counter)
                if isinstance(result, int):
                    counter = result
                    if counter == index:
                        return node.GetChild(child)
                if isinstance(result, cls_type):
                    return result
            if isinstance(node, cls_type):
                if counter == index:
                    return node
                else:
                    return counter


def FindByIndex(node, index):
    '''
    Method which finds child according to index. Applies only to nodes whose children are sorted into a dict,
    so if the current node's children are in a list it will recursively search - similarly if the index is not found
    in the current node's dictionary indexes.
    :param node: current node to search for
    :param index: index of child.
    :return:
    '''
    result = None
    if isinstance(node.children, dict):
        result = node.GetChild(index)
        if result is None:
            children = list(node.children.keys())
            child = 0
            while child < len(children) and result is None:
                key = children[child]
                result = FindByIndex(node.GetChild(key), index)
                if result is not None:
                    break
                child += 1
    else:
        child = 0
        while child < len(node.children) and result is None:
            result = FindByIndex(node.GetChild(child), index)
            if result is not None:
                break
            child += 1
    return result


def FindPosition(node, addition, index=0):
    '''
    Method to search for children according to their position in list. Similar functionality to above method,
    except this is for adding items to the tree according to the nodes limits on children or types of children they can have
    :param node: current node being searched
    :param addition: the thing being added
    :param index: index to search
    :return:
    '''
    if node is None:
        return None
    if type(addition) in node.rules:
        if len(node.children) < node.limit or node.limit == 0:
            return node
        else:
            if len(node.children) == 0:
                return None
            indexes = node.GetChildrenIndexes()
            result = FindPosition(
                node.GetChild(
                    indexes[index]),
                addition,
                index)
            if result is None:
                index += 1
            child = 0
            while result is None and child < len(indexes):
                result = FindPosition(
                    node.GetChild(
                        indexes[child]),
                    addition,
                    index)
                child += 1
            return result
    else:
        if len(node.children) == 0:
            return None
        indexes = node.GetChildrenIndexes()
        result = FindPosition(node.GetChild(indexes[index]), addition, index)
        if result is None:
            index += 1
        child = 0
        while result is None and child < len(node.children):
            result = FindPosition(
                node.GetChild(
                    indexes[child]),
                addition,
                index)
            child += 1
        return result


class Node(object):

    """This class is very generic, and has 3 attributes:

        - children: as with any tree it needs to have children

        - limit: the maximum amount of children before castcading to the next level

        - rules: the class instances allowed to be children of this object


        Optional inputs:

          limit: the maximum num of children the node can have. 0 for no limit.

          rules: list of class types this node can have as child objects.

        """

    def __init__(self, **kwargs):
        self.children = []
        '''list of child nodes belonging to this node'''

        if "limit" in kwargs:
            self.limit = kwargs["limit"]
            '''max number of children in list'''
        else:
            self.limit = 0
        self.item = None
        if "rules" in kwargs:
            self.rules = kwargs["rules"]
            '''list of types of nodes which are accepted as child nodes'''
        else:
            self.rules = []

    def PopAllChildren(self):
        '''
        Method to remove and return all children of current node

        :return: list of children
        '''
        indexes = self.GetChildrenIndexes()
        children = []
        for c in indexes:
            child = self.PopChild(c)
            children.append(child)
        return children

    def GetChildrenIndexes(self):
        '''
        Method to get a list of indexes at which children reside at

        :return: list of indexes
        '''
        indexes = list(range(len(self.children)))
        return indexes

    def SetItem(self, new_item):
        self.item = new_item

    def ReplaceChild(self, key, item):
        '''
        Method to remove child at <key> and replace it with <item>, then put the child back onto the end of the list

        :param key: index to position <item>

        :param item: child object to add

        :return:
        '''
        if key in self.GetChildrenIndexes():
            node = self.GetChild(key)
            children = node.GetChildrenIndexes()
            child_nodes = [(i, node.GetChild(i)) for i in children]
            self.children[key] = item
            [self.children[key].AddChild(kid[1], kid[0])
             for kid in child_nodes]

    def GetItem(self):
        return self.item

    def GetChild(self, index):
        if index == -1:
            index = len(self.children) - 1
            if index == -1:
                return None
        if index < len(self.children):
            return self.children[index]

    def AddChild(self, item, index=-1):
        """adds the child to the list - index is included as an optional param but doesn't do anything because
        this allows us to ducktype between this and IndexedNode """

        self.children.append(item)

    def PopChild(self, key):
        if key < len(self.children):
            return self.children.pop(key)

    def AddRule(self, rule):
        self.rules.append(rule)


class EmptyNode(Node):

    """This is a class used to represent gaps in note representation - i.e where we want to jump forward in the measure and then come back
    and fill the gap in later on. Used mostly in voices where we maybe want to fill in an extra voice at a specific moment"""

    def __init__(self, duration, **kwargs):
        limit = 0
        rules = []
        if "limit" in kwargs:
            limit = kwargs["limit"]
        if "rules" in kwargs:
            rules = kwargs["rules"]
        self.duration = duration
        Node.__init__(self, limit=limit, rules=rules)


class IndexedNode(Node):

    """same as node, except the children section have their own indexes. to be used in nodes like Piece and Part, as both have
    children which have indexes applied to them in xml"""

    def __init__(self, **kwargs):
        Node.__init__(self, **kwargs)
        self.__delattr__("children")
        self.children = {}
        '''dictionary of children attached to this node'''

    def PopChild(self, key):
        if key in self.children:
            return self.children.pop(key)

    def GetChildrenIndexes(self):
        return list(self.children.keys())

    def GetChild(self, index):
        if index in self.children:
            return self.children[index]

    def AddChild(self, item, index=-1):
        if index == -1:
            index = len(self.children) - 1
        self.children[index] = item


class Tree(object):

    """Your basic generic tree structure, but with a few improvements to handle automatic ruling."""

    def __init__(self):
        self.root = None
        '''The root node of the tree'''

    def AddNode(self, node, index=-1):
        if self.root is None:
            self.root = node
        else:
            position = FindPosition(self.root, node, 0)
            if position is None:
                raise CannotAddToTreeException
            else:
                position.AddChild(node, index=index)

    def FindNode(self, cls_type, index, id=None):
        result = Search(cls_type, self.root, index, start_index=0)
        if result is None:
            raise CannotFindInTreeException
        return result

    def FindNodeByIndex(self, index):
        return FindByIndex(self.root, index)
