from museparse.classes.ObjectHierarchy.TreeClasses.BaseTree import IndexedNode
from museparse.classes.ObjectHierarchy.TreeClasses import MeasureNode
from museparse.classes.ObjectHierarchy.ItemClasses import BarlinesAndMarkers


class StaffNode(IndexedNode):

    def __init__(self):
        IndexedNode.__init__(self, rules=[MeasureNode.MeasureNode])
        self.autoBeam = True

    def NewBeam(self, type):
        if type == "end":
            self.autoBeam = False

    def CheckTotals(self):
        measures = self.GetChildrenIndexes()
        total = "1"
        for m_id in measures:
            mNode = self.GetChild(m_id)
            mItemTotal = mNode.GetTotalValue()
            if mItemTotal == "":
                mNode.value = total
            else:
                total = mItemTotal
                mNode.value = mItemTotal

    def SortedChildren(self):
        children = self.GetChildrenIndexes()
        integers = [child for child in children if isinstance(child, int)]
        strings = [child for child in children if isinstance(child, str)]
        result = []
        integers.sort()
        waiting = []
        if len(strings) > 0:
            strings.sort()
            counter = 0
            str_counter = 0
            while counter < len(integers) or str_counter < len(strings):
                result.append(integers[counter])
                if str_counter < len(strings):
                    number = strings[str_counter][1:]
                    digit = int(number)
                    if digit == integers[counter]:
                        result.append(strings[str_counter])
                    else:
                        waiting.append((strings[str_counter][0], digit))
                result.extend([w[0] + str(w[1])
                               for w in waiting if integers[counter] == w[1]])
                counter += 1
                str_counter += 1
        else:
            result = integers

        return result

    def toLily(self):
        '''
        Method which converts the object instance, its attributes and children to a string of lilypond code

        :return: str of lilypond code
        '''

        lilystring = ""

        if not self.autoBeam:
            lilystring += "\\autoBeamOff"
        children = self.SortedChildren()
        if not hasattr(self, "transpose"):
            self.transpose = None
        for child in range(len(children)):
            measureNode = self.GetChild(children[child])
            measureNode.autoBeam = self.autoBeam
            lilystring += " % measure " + str(children[child]) + "\n"
            lilystring += measureNode.to_lily() + "\n\n"
        return lilystring

    def CheckDivisions(self):
        children = self.GetChildrenIndexes()
        divisions = 1
        for child in children:
            measure = self.GetChild(child)
            if hasattr(measure, "divisions"):
                divisions = measure.divisions
            else:
                measure.divisions = divisions
            measure.check_divisions()

    def DoBarlineChecks(self):
        measure_indexes = self.GetChildrenIndexes()
        if hasattr(self, "backward_repeats"):
            if len(self.backward_repeats) > 0:
                measure = self.GetChild(measure_indexes[0])
                for repeat in self.backward_repeats:
                    measure.AddBarline(
                        BarlinesAndMarkers.Barline(
                            repeat="forward",
                            repeatNum=repeat),
                        location="left-1")
        if hasattr(self, "forward_repeats"):
            if len(self.forward_repeats) > 0:
                measure = self.GetChild(measure_indexes[-1])
                for repeat in self.forward_repeats:
                    measure.AddBarline(
                        BarlinesAndMarkers.Barline(
                            repeat="backward",
                            repeatNum=repeat),
                        location="right-1")

    def AddBarline(self, item=None, measure_id=1, location="left"):
        measure = self.GetChild(measure_id)
        if measure is None:
            self.AddChild(MeasureNode.MeasureNode(), measure_id)
            measure = self.GetChild(measure_id)
        if hasattr(item, "repeat"):
            num = item.repeatNum
            if item.repeat == "forward":
                if not hasattr(self, "forward_repeats"):
                    self.forward_repeats = []
                self.forward_repeats.append(num)
            if item.repeat == "backward":
                num = item.repeatNum
                if not hasattr(self, "backward_repeat"):
                    self.backward_repeats = []
                self.backward_repeats.append(num)
                if hasattr(
                    self, "forward_repeats") and (
                    len(
                        self.forward_repeats) == len(
                        self.backward_repeats) and len(
                        self.forward_repeats) > 0):
                    self.forward_repeats.pop()
                    self.backward_repeats.pop()
        measure.AddBarline(item, location=location)
