from museparse.classes.ObjectHierarchy.TreeClasses.BaseTree import Node
from museparse.classes.ObjectHierarchy.TreeClasses import NoteNode
from museparse.classes.ObjectHierarchy.ItemClasses.Note import Arpeggiate, NonArpeggiate, GraceNote, Tuplet


class VoiceNode(Node):

    def __init__(self):
        Node.__init__(self, rules=[NoteNode.NoteNode, NoteNode.Placeholder])
        self.note_total = 0
        self.note_types = []

    def addNoteDuration(self, duration):
        self.note_total += duration
        self.note_types.append(duration)

    def removeNoteDuration(self, duration):
        self.note_total -= duration
        self.note_types.remove(duration)

    def GetAllNoteTypes(self):
        """ method to collect all note values from each node

        :return: list of note values
        """
        return self.note_types

    def RunNoteChecks(self):
        children = self.GetChildrenIndexes()
        previous = None
        for child in range(len(children)):
            note = self.GetChild(children[child])
            item = note.GetItem()
            if item is not None and isinstance(note, NoteNode.NoteNode):
                # look for arpeggiates or non-arpeggiates, and update the note's childnodes
                # used where a note is part of a chord (usually the case in
                # arpeggiates)
                arpeg = item.search(Arpeggiate)
                narpeg = item.search(NonArpeggiate)
                if arpeg is not None or narpeg is not None:
                    note.UpdateArpeggiates()

                # now look for gracenotes
                result = item.search(GraceNote)
                if result is not None and previous is None:
                    # if this is the first note in the bar, it must be the
                    # first gracenote
                    result.first = True

                if len(children) == child + 1:
                    # if we're at the last note...
                    if result is not None:
                        # same check as arpeggiates - handles the case where
                        # notes are part of a chord
                        note.CheckForGraceNotes()

                    # look for timemods
                    if hasattr(item, "timeMod"):
                        result = item.search(Tuplet)
                        if result is None:
                            item.close_timemod = True
                        if previous is not None:
                            if hasattr(previous.GetItem(), "timeMod"):
                                item.timeMod.first = False
                            else:
                                item.timeMod.first = True
                        else:
                            item.timeMod.first = True
                    else:
                        item.close_timemod = False
                else:
                    # otherwise check the next item for gracenotes and time
                    # mods
                    next = self.GetChild(children[child + 1])
                    next_item = next.GetItem()
                    if next_item is not None and isinstance(
                            next,
                            NoteNode.NoteNode):
                        result = item.search(GraceNote)
                        next_result = next_item.search(GraceNote)
                        if result is not None:
                            if next_result is None:
                                note.CheckForGraceNotes()
                            else:
                                result.last = False
                                next_result.first = False
                        if hasattr(item, "timeMod"):
                            res = item.search(Tuplet)

                            if not hasattr(
                                    next_item,
                                    "timeMod") and res is None:
                                item.close_timemod = True
                            else:
                                item.close_timemod = False

                            # not sure if checking next and previous is
                            # necessary?
                            if previous is not None and isinstance(
                                    previous,
                                    NoteNode.NoteNode):
                                if hasattr(previous.GetItem(), "timeMod"):
                                    item.timeMod.first = False
                                else:
                                    item.timeMod.first = True
                            else:
                                item.timeMod.first = True
            previous = note

    def toLily(self):
        '''
        Method which converts the object instance, its attributes and children to a string of lilypond code

        :return: str of lilypond code
        '''

        lilystring = ""
        children = self.GetChildrenIndexes()
        total = self.note_total
        counter = 0
        for child in range(len(children)):
            note = self.GetChild(children[child])
            item = note.GetItem()
            if item is not None:
                item.autoBeam = self.autoBeam
            if hasattr(note, "duration"):
                try:
                    counter += int(note.duration)
                except:
                    if note.duration == "\\longa":
                        counter += 0.25
                    if note.duration == "\\breve":
                        counter += 0.5
            if counter > total / 2:
                if hasattr(self, "mid_barline"):
                    lilystring += self.mid_barline.to_lily()
                    self.__delattr__("mid_barline")
            if hasattr(self, "rest") and hasattr(self, "total"):
                lilystring += "R" + self.total
            else:
                lilystring += note.to_lily() + " "
        return lilystring
