
from museparse.classes.ObjectHierarchy.TreeClasses.BaseTree import IndexedNode
from museparse.classes.ObjectHierarchy.ItemClasses import Part
from museparse.classes.ObjectHierarchy.TreeClasses import MeasureNode
from museparse.classes.ObjectHierarchy.TreeClasses.StaffNode import StaffNode

from museparse import helpers


class PartNode(IndexedNode):
    """
    Class representing the node holding the part.
    """

    def __init__(self, index=0):
        IndexedNode.__init__(self, rules=[StaffNode])
        self.index = index
        if self.item is None:
            self.item = Part.Part()

    def NewBeam(self, type, staff):
        staff_obj = self.getStaff(staff)
        staff_obj.NewBeam(type)

    def Backup(self, measure_id, duration=0):
        staves = self.GetChildrenIndexes()
        for staff_id in staves:
            staff = self.GetChild(staff_id)
            measure = staff.GetChild(measure_id)
            if measure is not None:
                measure.Backup(duration=duration)

    def Forward(self, measure_id, duration=0):
        staves = self.GetChildrenIndexes()
        for staff_id in staves:
            staff = self.GetChild(staff_id)
            measure = staff.GetChild(measure_id)
            if measure is not None:
                measure.Forward(duration=duration)

    def AddBarline(self, staff=1, measure=1, location="left", item=None):
        staff_obj = self.getStaff(staff)
        if staff_obj is None:
            self.AddChild(StaffNode(), staff)
            staff_obj = self.getStaff(staff)
        staff_obj.AddBarline(measure_id=measure, location=location, item=item)

    def DoBarlineChecks(self):
        staves = self.GetChildrenIndexes()
        for s in staves:
            staff = self.getStaff(s)
            staff.DoBarlineChecks()

    def CheckDivisions(self):
        staves = self.GetChildrenIndexes()
        for staff in staves:
            child = self.getStaff(staff)
            child.check_divisions()

    def CheckTotals(self):
        """method to calculate the maximum total lilypond value for a measure without a time signature"""
        staves = self.GetChildrenIndexes()
        for staff in staves:
            child = self.getStaff(staff)
            child.CheckTotals()

    def CheckMeasureDivisions(self, measure):
        divisions = None
        staves = self.GetChildrenIndexes()
        for staff in staves:
            measure_obj = self.getMeasure(measure, staff)
            if measure_obj is not None:
                if hasattr(measure_obj.GetItem(), "divisions"):
                    divisions = measure_obj.GetItem().divisions
                elif divisions is not None:
                    measure_obj.GetItem().divisions = divisions

    def CheckPreviousBarline(self, staff):
        """method which checks the bar before the current for changes we need to make to it's barlines"""
        measure_before_last = self.getMeasureAtPosition(-2, staff)
        last_measure = self.getMeasureAtPosition(-1, staff)
        if last_measure is not None and measure_before_last is not None:
            bline1 = measure_before_last.GetBarline("right")
            bline2 = last_measure.GetBarline("left")
            if bline1 is not None:
                if hasattr(bline1, "ending"):
                    if bline2 is not None:
                        if not hasattr(bline2, "ending"):
                            bline1.ending.type = "discontinue"
                    else:
                        bline1.ending.type = "discontinue"

    def CheckMeasureMeter(self, measure):
        meter = None
        staves = self.GetChildrenIndexes()
        for staff in staves:
            measure_obj = self.getMeasure(measure, staff)
            if measure_obj is not None:
                item = measure_obj.GetItem()
                if hasattr(item, "meter"):
                    meter = item.meter
                else:
                    if meter is not None:
                        item.meter = meter

    def setDivisions(self, measure=1, divisions=1):
        staves = self.GetChildrenIndexes()
        for staff in staves:
            measure_obj = self.getMeasure(measure, staff)
            measure_obj.GetItem().divisions = divisions

    def getMeasure(self, measure=1, staff=1):
        staff_obj = self.GetChild(staff)
        measure_obj = None
        if staff_obj is not None:
            measure_obj = staff_obj.GetChild(measure)
        return measure_obj

    def getMeasureAtPosition(self, index, staff=1):
        staff_obj = self.getStaff(staff)
        children = staff_obj.GetChildrenIndexes()
        if abs(index) <= len(children):
            return self.getMeasure(children[index], staff)

    def getMeasureIDAtPosition(self, index, staff=1):
        staff_obj = self.getStaff(staff)
        children = staff_obj.GetChildrenIndexes()
        if abs(index) <= len(children):
            return children[index]

    def getStaff(self, key):
        return self.GetChild(key)

    def addMeasure(self, item, measure=1, staff=1):
        if self.getStaff(staff) is None:
            self.AddChild(StaffNode(), staff)
        staff_obj = self.getStaff(staff)
        staff_obj.AddChild(item, measure)

    def addEmptyMeasure(self, measure=1, staff=1):
        self.addMeasure(
            MeasureNode.MeasureNode(),
            measure=measure,
            staff=staff)

    def CalculateVariable(self, name, staves):
        variables = []
        for staff in staves:
            variable = ""
            if len(name) > 0:
                lcase = name.lower()
                no_spaces = lcase.replace(' ', '')
                no_dots = no_spaces.replace('.', '')
                variable = ""
                for letter in no_dots:
                    if letter in [str(i) for i in range(10)]:
                        variable += helpers.NumbersToWords(int(letter))
                    else:
                        variable += letter
            variable += "staff" + helpers.NumbersToWords(staff)
            variables.append(variable)
        return variables

    def addKey(self, item, measure_id):
        staves = self.GetChildrenIndexes()
        for staff_id in staves:
            measure = self.getMeasure(measure_id, staff_id)
            if measure is not None:
                measure.addKey(item)
            else:
                self.addEmptyMeasure(measure_id, staff_id)
                measure = self.getMeasure(measure_id, staff_id)
                if measure is not None:
                    measure.addKey(item)

    def addClef(self, item, measure_id, staff_id, voice):
        measure = self.getMeasure(measure_id, staff_id)
        if measure is not None:
            measure.addClef(item, voice)
        else:
            self.addEmptyMeasure(measure_id, staff_id)
            measure = self.getMeasure(measure_id, staff_id)
            if measure is not None:
                measure.addClef(item)
        if item.sign == "percussion":
            self.drum = True
        else:
            self.drum = False
        if item.sign == "tab":
            self.tab = True
        else:
            self.tab = False

    def CheckIfTabStaff(self):
        if hasattr(self, "tab") and self.tab:
            return "TAB"
        if hasattr(self, "drum") and self.drum:
            return "DRUM"

    def toLily(self):
        '''
        Method which converts the object instance, its attributes and children to a string of lilypond code

        :return: str of lilypond code
        '''
        self.CheckDivisions()
        self.CheckTotals()
        staves = self.GetChildrenIndexes()
        name = ""
        shortname = ""
        if hasattr(self.item, "name"):
            name = self.item.name
            name = helpers.SplitString(name)
        if hasattr(self.item, "shortname"):
            shortname = helpers.SplitString(self.item.shortname)
        variables = self.CalculateVariable(str(self.index), staves)
        first_part = ""
        for staff, variable in zip(staves, variables):
            staffstring = variable
            if hasattr(
                    self.GetChild(staff),
                    "tab") and self.GetChild(staff).tab:
                staffstring += " = \\new TabStaff"
            elif hasattr(self.GetChild(staff), "drum") and self.GetChild(staff).drum:
                staffstring += " = \\drums"
            else:
                staffstring += " = \\new Staff"
            if len(staves) == 1:
                if name != "":
                    staffstring += " \with {\n"
                    staffstring += "instrumentName = " + name + " \n"
                    if shortname != "":
                        staffstring += "shortInstrumentName = " + \
                            shortname + " \n"
                    staffstring += " }"
            staffstring += "{" + self.GetChild(staff).to_lily() + " }\n\n"
            first_part += staffstring

        second_part = ""
        if len(variables) > 1:
            second_part += "\\new StaffGroup "
            if name != "":
                second_part += "\with {\n"
                second_part += "instrumentName = " + name + " \n"
                second_part += " }"
            second_part += "<<"
        second_part += "\n".join(["\\" + var for var in variables])
        if len(variables) > 1:
            second_part += ">>"
        return [first_part, second_part]
