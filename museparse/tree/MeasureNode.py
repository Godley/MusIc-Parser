import copy

from museparse.tree.basetree import IndexedNode, BackwardSearch, Search

from museparse.tree.voicenode import VoiceNode
from museparse.tree.othernodes import DirectionNode, ExpressionNode, KeyNode, ClefNode
from museparse.tree.notenode import NoteNode
from museparse.elements import directions
from museparse import helpers
from museparse.elements.directions import OctaveShift


class MeasureNode(IndexedNode):

    """
    Class representing the tree node for a measure.


    # Optional inputs:

        - partial: bool. Represents whether the bar is partial i.e a pickup or something


    # Optional attributes:

        - newSystem: boolean indicating to create a new system for this bar

        - newPage: boolean indicating to create a new page for this bar

        - key: Key class entry representing key sig

        - meter: meter class entry representing meter/time sig
    """

    def __init__(self, **kwargs):
        IndexedNode.__init__(self, rules=[VoiceNode])
        self.index = 0
        self.barlines = {}
        self.items = []
        self.autoBeam = False
        if "partial" in kwargs:
            if kwargs["partial"] is not None:
                self.partial = kwargs["partial"]
        self.gap = 0

    def addWrapper(self, item):
        # method to add any notation that needs to wrap the whole bar
        self.items.append(item)

    def CalculateTransposition(self):
        scale = [
            'a',
            'bes',
            'b',
            'c',
            'cis',
            'd',
            'dis',
            'e',
            'f',
            'fis',
            'g',
            'gis']
        base = 3
        result = base
        octave_shifters = "'"
        if hasattr(self.transpose, "chromatic"):
            chromatic = int(self.transpose.chromatic)
            result = base + chromatic

        elif hasattr(self.transpose, "diatonic"):
            diatonic = int(self.transpose.diatonic)
            result = base + (diatonic * 2)

        if result < 0:
            result = (len(scale) - 1) - result
            octave_shifters = ""
        if result >= len(scale):
            result = result - (len(scale) - 1)
            octave_shifters += "'"
        lettername = scale[result]

        if hasattr(self.transpose, "octave"):
            octave = self.transpose.octave

            if octave > 0:
                octave_shifters += "".join(["'" for i in range(octave)])
            if octave < 0:
                octave_shifters = ""
                if octave < -1:
                    octave_shifters += "".join(
                        ["," for i in range(abs(octave))])
        return "\\transpose c' " + lettername + octave_shifters + " {"

    def HandleAttributes(self):
        lilystring = ""
        if hasattr(self, "newSystem"):
            lilystring += "\\break "
        if hasattr(self, "newPage"):
            lilystring += "\\pageBreak "
        if hasattr(self, "clef") and self.clef is not None:
            lilystring += self.clef.to_lily() + " "
        if hasattr(self, "key") and self.key is not None:
            if not hasattr(self.key, "mode"):
                self.key.mode = "major"
            lilystring += self.key.to_lily() + " "
        if hasattr(self, "meter"):
            lilystring += self.meter.to_lily() + " "
        if hasattr(self, "partial") and self.partial:
            lilystring += "\\partial " + str(self.getPartialLength()) + " "
        for item in self.items:
            if not hasattr(
                item,
                "type") or (
                hasattr(
                    item,
                    "type") and item.type != "stop"):
                lilystring += item.to_lily()
        return lilystring

    def HandleClosingAttributes(self):
        lstring = ""
        for item in self.items:
            if hasattr(item, "type") and item.type == "stop":
                lstring += item.to_lily()

        return lstring

    def getWrapper(self, index):
        if index < len(self.items):
            return self.items[index]

    def GetTotalValue(self):
        """Gets the total value of the bar according to it's time signature"""
        value = ""
        if hasattr(self, "meter"):
            top_value = self.meter.beats
            bottom = self.meter.type
            fraction = top_value / bottom
            if fraction == 1:
                value = "1"
            else:
                if fraction > 1:
                    value = "1."
                if fraction < 1:
                    if fraction >= 0.5:
                        fraction -= 0.5
                        value = "2"
                        if fraction == 0.25:
                            value += "."
        return value

    def AddBarline(self, item, location):
        if location != "left" and location != "right" and location != "center":
            if location not in self.barlines:
                self.barlines[location] = []
            self.barlines[location].append(item)
        else:
            self.barlines[location] = item

    def GetBarline(self, location):
        if location in self.barlines:
            return self.barlines[location]

    def GetLastKey(self, voice=1):
        """key as in musical key, not index"""

        voice_obj = self.GetChild(voice)
        if voice_obj is not None:
            key = BackwardSearch(KeyNode, voice_obj, 1)
            if key is not None:
                return key
            else:
                if hasattr(self, "key"):
                    return self.key
        else:
            if hasattr(self, "key"):
                return self.key

    def addKey(self, item, voice=1):
        if not hasattr(self, "key"):
            self.key = item
        else:
            if self.GetChild(voice) is None:
                self.addVoice(VoiceNode(), voice)
            voice_obj = self.GetChild(voice)
            node = KeyNode()
            node.SetItem(item)
            if voice_obj is not None:
                voice_obj.AddChild(node)
                self.index += 1

    def GetLastClef(self, voice=1):
        if self.GetChild(voice) is None:
            self.addVoice(VoiceNode(), voice)
        voice_obj = self.GetChild(voice)
        if voice_obj is not None:
            key = BackwardSearch(ClefNode, voice_obj, 1)
            if key is not None:
                return key
            else:
                if hasattr(self, "clef"):
                    return self.clef

    def addClef(self, item, voice=1):
        '''
        method to use when adding a clef. will either add it to the node itself or add it onto the first voice's children
        list
        :param item:
        :param voice:
        :return:
        '''
        if not hasattr(self, "clef"):
            self.clef = item
        else:
            voice_obj = self.GetChild(voice)
            node = ClefNode()
            node.SetItem(item)
            if voice_obj is not None:
                voice_obj.AddChild(node)
                self.index += 1

    def CheckDivisions(self):
        children = self.GetChildrenIndexes()
        divisions = self.divisions
        for child in children:
            voice = self.GetChild(child)
            indexes = voice.GetChildrenIndexes()
            for i in indexes:
                note = voice.GetChild(i)
                item = note.GetItem()
                if item is not None:
                    item.divisions = divisions

    def Forward(self, duration=0):
        '''
        method to use when forward tag is encountered in musicXML. jumps forward in the bar by <duration>
        :param duration: number of beats to move forward
        :return:
        '''
        for voice in self.GetChildrenIndexes():
            voice_obj = self.getVoice(voice)
            if voice_obj.GetChild(self.index) is None:
                voice_obj.AddChild(NoteNode.NoteNode(duration=duration))
        self.index += 1

    def Backup(self, duration=0):
        '''
        method to use when a backup tag is encountered in musicXML. Moves back in the bar by <duration>
        :param duration:
        :return:
        '''
        total = 0
        duration_total = duration * 4
        children = self.GetChildrenIndexes()
        notes = 0
        for voice in children:
            v = self.GetChild(voice)
            indexes = v.GetChildrenIndexes()
            if len(indexes) > 1:
                indexes.reverse()
            for index in indexes:
                notes += 1
                note = v.GetChild(index)
                if hasattr(note, "duration"):
                    total += note.duration
                    if total >= duration_total:
                        break
            gap = [
                v.GetChild(i).duration for i in range(
                    0,
                    self.index -
                    notes) if hasattr(
                    v.GetChild(i),
                    "duration")]
            previous = 0
            for item in gap:
                if item == previous:
                    self.gap -= previous
                    item = item / 2
                self.gap += item
                previous = item
            #self.gap = sum([])
        self.index -= notes

    def addVoice(self, item=None, id=1):
        if item is None:
            item = VoiceNode()
        self.AddChild(item, id)
        if self.gap != 0:
            voice = self.GetChild(id)
            voice.AddChild(NoteNode.Placeholder(duration=self.gap))
            self.gap = 0

    def getVoice(self, key):
        return self.GetChild(key)

    def PositionChild(self, item, key, voice=1):
        voice_obj = self.getVoice(voice)
        children = voice_obj.GetChildrenIndexes()
        if key in children:
            start_index = key
            end_index = len(children)
            popped = []
            for index in range(start_index, end_index):
                child = voice_obj.PopChild(index)
                if child is not None:
                    popped.append(child)
            voice_obj.AddChild(item)
            [voice_obj.AddChild(p) for p in popped]

    def addNote(self, item, voice=1, increment=1, chord=False):
        shift = 0
        # get the appropriate voice
        if self.getVoice(voice) is None:
            self.addVoice(VoiceNode(), voice)
        voice_obj = self.getVoice(voice)
        last = voice_obj.GetChild(self.index - 1)
        if last is not None and hasattr(last, "shift"):
            shift = True
        # set up a basic duration: this val will only be used for a placeholder
        duration = 0
        if not isinstance(
                item,
                NoteNode.NoteNode) and not isinstance(
                item,
                NoteNode.Placeholder):
            # wrap the item in a node if it isn't wrapped already
            if hasattr(item, "duration"):
                duration = item.duration

            node = NoteNode.NoteNode(duration=duration)
            node.SetItem(item)
            if shift != 0:
                node.shift = shift
        else:
            node = item
            if hasattr(node, "duration"):
                duration = node.duration
        if not chord:
            try:
                voice_obj.addNoteDuration(int(duration))
            except:
                if duration == "\\longa":
                    voice_obj.addNoteDuration(0.25)
                if duration == "\\breve":
                    voice_obj.addNoteDuration(0.5)
            # get whatever is at the current index
            placeholder = voice_obj.GetChild(self.index)
            if isinstance(
                    placeholder,
                    NoteNode.Placeholder) and not isinstance(
                    node,
                    NoteNode.Placeholder):
                # if it's an empty placeholder, replace it with a note
                if placeholder.duration == 0:
                    if hasattr(placeholder, "shift"):
                        children = placeholder.GetChildrenIndexes()
                        # this will need some recursion if we have multiple directions attached to a placeholder,
                        # but for now this should work.
                        for c in children:
                            child = placeholder.GetChild(c)
                            if child.GetItem(
                            ).__class__.__name__ == OctaveShift.__name__:
                                i = placeholder.PopChild(c)
                                voice_obj.ReplaceChild(
                                    self.index,
                                    copy.deepcopy(i))
                                self.index += 1
                    if voice_obj.GetChild(self.index) == placeholder:
                        voice_obj.ReplaceChild(self.index, node)
                    elif voice_obj.GetChild(self.index) is not None:
                        self.PositionChild(node, self.index, voice=voice)
                    else:
                        voice_obj.AddChild(node, self.index)
                    if not isinstance(node, NoteNode.Placeholder):
                        self.index += 1

            # nothing there? add our note
            elif placeholder is None:
                voice_obj.AddChild(node)
                if not isinstance(node, NoteNode.Placeholder):
                    self.index += 1
            else:
                proposed_node = voice_obj.GetChild(self.index)
                new_duration = voice_obj.GetChild(self.index).duration
                if proposed_node.GetItem() is None:
                    if hasattr(item, "duration"):
                        new_duration = item.duration
                    if new_duration == proposed_node.duration:
                        node.SetItem(node.GetItem())
                        voice_obj.removeNoteDuration(proposed_node.duration)
                        voice_obj.ReplaceChild(self.index, node)
                    elif new_duration > proposed_node.duration:
                        proposed_node.SetItem(node.GetItem())
                        proposed_node.duration = new_duration
                        voice_obj.removeNoteDuration(proposed_node.duration)
                    elif new_duration < proposed_node.duration:
                        voice_obj.removeNoteDuration(proposed_node.duration)
                        voice_obj.removeNoteDuration(new_duration)
                        proposed_node.duration -= new_duration
                        voice_obj.addNoteDuration(proposed_node.duration)
                        voice_obj.addNoteDuration(new_duration)
                        voice_obj.AddChild(node)
                        if not isinstance(node, NoteNode.Placeholder):
                            self.index += 1
                else:
                    self.PositionChild(node, self.index, voice=voice)

        else:
            # get whatever is at the current index
            placeholder = voice_obj.GetChild(self.index - 1)
            if placeholder.GetItem() is not None:
                if hasattr(placeholder.GetItem(), "beams"):
                    node.GetItem().beams = placeholder.GetItem().beams
            if placeholder is not None:
                placeholder.AttachNote(node)

    def getPartialLength(self):
        """ method to calculate how much to give the "partial" indicator where a measure is a pickup
        :return: str which is the lilypond bar length
        """
        indexes = self.GetChildrenIndexes()
        length = 0
        divider = 0
        total = 0
        result = ""
        for v in indexes:
            voice = self.GetChild(v)
            if voice.note_total > length:
                length = voice.note_total
                note_types = voice.GetAllNoteTypes()
                if len(note_types) == 1:
                    total = length
                    result = str(total)
                else:
                    note_types.sort()
                    total = note_types[0]
                    result = str(total)
                    previous = total
                    count = 0
                    for value in note_types[1:]:
                        if previous * 2 == value:
                            result += "."
                        if previous == value:
                            if total >= previous:
                                total -= previous
                            else:
                                total -= previous / 2
                            total += previous / 2
                            value = previous / 2
                        previous = value

                    first_digit = str(int(total))
                    result = first_digit + result[1:]

        return result

    def addPlaceholder(self, duration=0, voice=1):
        holder = NoteNode.Placeholder(duration=duration)
        if self.getVoice(voice) is None:
            self.addVoice(VoiceNode(), voice)
        voice_obj = self.getVoice(voice)
        children = voice_obj.GetChildrenIndexes()
        if self.index >= len(children):
            self.addNote(holder, voice)
        else:
            self.PositionChild(holder, self.index, voice=voice)
        return None

    def addDirection(self, item, voice=1):
        wrappers = [directions.Bracket.__name__]
        if item.__class__.__name__ in wrappers and (
            not hasattr(
                item,
                "type") or (
                hasattr(
                item,
                "type") and item.type != "start")):
            self.addWrapper(item)
            return
        if item.__class__.__name__ in wrappers and hasattr(
                item,
                "type") and item.type == "start":
            if hasattr(item, "lineType"):
                copy_obj = copy.deepcopy(item)
                copy_obj.type = ""
                item.lineType = ""
                self.addWrapper(copy_obj)

        if self.getVoice(voice) is None:
            self.addVoice(VoiceNode(), voice)
        direction_obj = DirectionNode()
        direction_obj.SetItem(item)
        voice_obj = self.getVoice(voice)
        if self.index == 0:
            finder = 0
        else:
            if item.__class__.__name__ == directions.Pedal.__name__:
                note = voice_obj.GetChild(self.index - 1)
                if note is not None:
                    result = note.Find(DirectionNode, directions.Pedal)
                    if result is not None:
                        self.index += 1
            finder = self.index

        note_obj = voice_obj.GetChild(finder)
        if isinstance(
                note_obj,
                NoteNode.NoteNode) or isinstance(
                note_obj,
                NoteNode.Placeholder):
            note_obj.AttachDirection(direction_obj)
        else:
            self.addPlaceholder()
            if self.index >= len(voice_obj.children):
                self.index = len(voice_obj.children) - 1
            note_obj = voice_obj.GetChild(self.index)
            if isinstance(note_obj, NoteNode.Placeholder):
                note_obj.AttachDirection(direction_obj)

    def addExpression(self, item, voice=1):
        if self.getVoice(voice) is None:
            self.addVoice(VoiceNode(), voice)
        direction_obj = ExpressionNode()
        direction_obj.SetItem(item)
        voice_obj = self.getVoice(voice)
        note_obj = voice_obj.GetChild(self.index)
        if isinstance(
                note_obj,
                NoteNode.NoteNode) or isinstance(
                note_obj,
                NoteNode.Placeholder):
            note_obj.AttachExpression(direction_obj)
        else:
            self.addPlaceholder()
            note_obj = voice_obj.GetChild(self.index)
            if isinstance(note_obj, NoteNode.Placeholder):
                note_obj.AttachExpression(direction_obj)

    def toLily(self):
        '''
        Method which converts the object instance, its attributes and children to a string of lilypond code

        :return: str of lilypond code
        '''
        lilystring = ""
        left_barline = self.GetBarline("left")
        other_lefts = self.GetBarline("left-1")
        if other_lefts is not None:
            for left in other_lefts:
                lilystring += left.to_lily()

        if left_barline is not None:
            lilystring += left_barline.to_lily()

        lilystring += self.HandleAttributes()
        voices = self.GetChildrenIndexes()

        if not hasattr(self, "value"):
            self.value = self.GetTotalValue()
        if len(voices) > 1:
            lilystring += "<<"
        for voice in voices:
            mid_barline = self.GetBarline("middle")
            v_obj = self.getVoice(voice)
            v_obj.autoBeam = self.autoBeam
            if mid_barline is not None:
                v_obj.mid_barline = mid_barline[0]
            v_obj.total = self.value
            if len(voices) > 1:
                lilystring += " % voice " + str(voice) + "\n"
                lilystring += "\\new Voice = \"" + \
                    helpers.NumbersToWords(voice) + "\"\n"
                lilystring += "{\\voice" + \
                    helpers.NumbersToWords(voice).capitalize() + " "
            lilystring += v_obj.to_lily()
            if len(voices) > 1:
                lilystring += "}"
        if len(voices) > 1:
            lilystring += ">>"
        lilystring += self.HandleClosingAttributes()
        right_barline = self.GetBarline("right")
        other_rights = self.GetBarline("right-1")
        if other_rights is not None:
            for right in other_rights:
                lilystring += right.to_lily()

        if right_barline is not None:
            lilystring += right_barline.to_lily()
        else:
            lilystring += " | "
        return lilystring

    def CopyDirectionsAndExpressions(self, v_obj):
        child = self.GetChildrenIndexes()[0]
        voice = self.GetChild(child)
        voice_notes = v_obj.GetChildrenIndexes()
        for n in voice_notes:
            note = v_obj.GetChild(n)
            new_position = voice.GetChild(n)
            if new_position is not None:
                children_to_add = note.PopAllChildren()
                for child in children_to_add:
                    if isinstance(child, NoteNode.NoteNode):
                        new_position.AttachNote(child)
                    if isinstance(child, ExpressionNode):
                        new_position.AttachExpression(child)
                    if isinstance(child, DirectionNode):
                        new_position.AttachDirection(child)

    def RunVoiceChecks(self):
        children = self.GetChildrenIndexes()

        if len(children) > 1:
            for child in children:
                voice = self.GetChild(child)
                total = voice.note_total
                result = Search(NoteNode.NoteNode, voice, 1)
                if result is None or total == 0:
                    voice = self.PopChild(child)
                    self.CopyDirectionsAndExpressions(voice)
                voice.RunNoteChecks()
        else:
            voice = self.GetChild(1)
            if voice is not None:
                voice.RunNoteChecks()
