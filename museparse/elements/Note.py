import math

from museparse.elements import baseclass, mark, ornaments


class Tie(baseclass.Base):
    """
    Class representing a tie.

    Optional inputs:
        type: either start or stop. Stop isn't particularly useful to lilypond but may be used in other output formats.
    """

    def __init__(self, type):
        super().__init__()
        if type is not None:
            self.type = type

    def to_lily(self):
        lily = ""
        if hasattr(self, "type"):
            if self.type == "start":
                lily = "~"
        return lily


class Notehead(baseclass.Base):

    """
    Class representing noteheads.
    Optional inputs:
        filled: whether or not the notehead is filled. bool.
        type: type of notehead. str.
    """

    def __init__(self, filled=False, type=""):
        super().__init__()
        self.filled = filled
        self.type = type

    def to_lily(self):
        pre_note = "\n\\tweak #'style #'"
        if self.type != "":
            ignore = [
                "slashed",
                "back slashed",
                "inverted triangle",
                "arrow up",
                "arrow down",
                "normal"]
            if self.type == "diamond":
                val = "\\harmonic"
                return [val]
            if self.type == "x":
                val = "\\xNote"
                return [val, ""]
            options = {
                "diamond": "harmonic",
                "x": "cross",
                "circle-x": "xcircle"}
            if self.type in options:
                pre_note += options[self.type]
            elif self.type not in ignore:
                pre_note += self.type
            if self.type in ignore:
                pre_note = ""
                val = ""
        else:
            pre_note = ""

        return [pre_note + "\n", ""]


class Stem(baseclass.Base):

    """
    Class representing the note's stem.
    optional input:
        type: type of stem to show
    """

    def __init__(self, type):
        if type is not None:
            self.type = type
        baseclass.Base.__init__(self)

    def __str__(self):
        return self.type

    def to_lily(self):
        val = "\n\stem"
        if not hasattr(self, "type"):
            val += "Neutral"
        else:
            val += self.type[0].upper() + self.type[1:len(self.type)]
        return val


class Pitch(baseclass.Base):

    """
    Class representing the pitch of the note

    Optional inputs:
        alter: how many semi tones to raise or lower the pitch. Generally either 1 or -1, float.
        octave: number of the octave in which it resides in. int
        accidental: accidental to show. Used where alter is not accurate enough, may indicate any range of accidentals such as
                double sharps etc.
        unpitched: bool representation of unpitchedness, aka a pitch which is like a clap or something rather than an actual note.
    """

    def __init__(self, **kwargs):
        if "alter" in kwargs:
            self.alter = kwargs["alter"]
        if "octave" in kwargs:
            self.octave = int(kwargs["octave"])
        if "step" in kwargs:
            self.step = kwargs["step"]
        if "accidental" in kwargs:
            self.accidental = kwargs["accidental"]
        if "unpitched" in kwargs:
            self.unpitched = True
        baseclass.Base.__init__(self)

    def __str__(self):
        st = ""
        alter = {1: "sharp", -
                 1: "flat", 0: "", 2: "double-sharp", -
                 2: "double-flat"}
        if hasattr(self, "unpitched"):
            st += "unpitched"
        if hasattr(self, "step"):
            st += self.step

        if hasattr(self, "alter"):
            st += alter[int(self.alter)]
        if hasattr(self, "accidental"):
            st += "(" + self.accidental + ")"
        if hasattr(self, "octave"):
            st += self.octave
        return st

    def to_lily(self):
        val = ""
        if not hasattr(self, "step"):
            val += "c"
        else:
            val += self.step.lower()
        if hasattr(self, "alter"):
            if self.alter == 1:
                val += "is"
            elif self.alter == -1:
                val += "es"
        if hasattr(self, "accidental"):
            names = {
                "three-quarters-sharp": "isih",
                "three-quarters-flat": "eseh",
                "quarter-sharp": "ih",
                "quarter-flat": "eh",
                "flat-flat": "eses",
                "double-sharp": "isis"}
            if self.accidental in names:
                val += names[self.accidental]
        if not hasattr(self, "octave"):
            val += "'"
        else:
            oct = int(self.octave)
            if oct > 3:
                for i in range(oct - 3):
                    val += "'"
            elif oct < 3:
                counter = 3 - oct
                while counter != 0:
                    val += ","
                    counter -= 1

        return val


class Note(baseclass.Base):

    """
    Big class representing a note.

    Optional inputs:
        rest: bool as to whether this note is a rest or not.
        dots: int - number of dots after the note, indicating extended length
        pitch: a class representing the pitch of the note, see above
        chord: bool indicating this note is part of a chord
        type: string indicator of the length of note, like "quarter" or "half". Alternatively, duration may be given along with divisions
        duration: length of note. Where musicXML is concerned, divisions should also be known, indicating how many divisions there are in
            a quarter note.


    """

    def __init__(self, **kwargs):
        baseclass.Base.__init__(self)
        self.ties = []
        self.beams = {}
        if "rest" in kwargs:
            self.rest = kwargs["rest"]
        else:
            self.rest = False
        if "dots" in kwargs:
            self.dots = kwargs["dots"]
        else:
            self.dots = 0
        if "pitch" in kwargs:
            self.pitch = kwargs["pitch"]
        if "chord" in kwargs and kwargs["chord"] is not None:
            self.chord = kwargs["chord"]
        if "type" in kwargs and kwargs["type"] is not None:
            self.set_type(kwargs["type"])
        elif "duration" in kwargs:
            self.duration = kwargs["duration"]
        if "divisions" in kwargs and kwargs["divisions"] is not None:
            self.divisions = float(kwargs["divisions"])
        self.prenotation = []
        '''any notation classes which come before the note is displayed - list'''

        self.wrap_notation = []
        '''any notation classes which have something to come before and something after the note is displayed - list'''

        self.postnotation = []
        '''notation to be shown after the note - list'''

        self.closing_notation = []
        '''notation to be shown after post notation - list'''

        self.has_tremolo = False

    def add_slur(self, item):
        '''
        Very simple method which is used for adding slurs.
        :param item:
        :return:
        '''
        if not hasattr(self, "slurs"):
            self.slurs = []
        self.slurs.append(item)

    def get_all_notation(self):
        return self.prenotation, self.wrap_notation, self.postnotation

    def get_notation(self, id, type):
        '''
        method which searches for notation from <type> list at position <id>
        :param id: the number to look for - i.e if you're looking for the first one in wrap notation, id will be 0
        :param type: post, pre or wrap
        :return: the notation class searched for or none
        '''
        if type == "post":
            if (id == -
                1 and len(self.postnotation) > 0) or (id != -
                                                      1 and len(self.postnotation) > id):
                return self.postnotation[id]
        if type == "pre":
            if (id == -
                1 and len(self.prenotation) > 0) or (id != -
                                                     1 and len(self.postnotation) > id):
                return self.prenotation[id]
        if type == "wrap":
            if (id == -
                1 and len(self.wrap_notation) > 0) or (id != -
                                                       1 and len(self.postnotation) > id):
                return self.wrap_notation[id]

    def flush_notation(self):
        self.prenotation = []
        self.wrap_notation = []
        self.postnotation = []
        self.closing_notation = []

    def get_closing_notation_as_lilypond(self):
        '''
        Converts notation in closing_notation into a lilypond string.
        :return: str
        '''
        lstring = ""
        for notation in self.closing_notation:
            result = notation.to_lily()
            if type(result) == list:
                result = "".join(result)
            lstring += result
        return lstring

    def add_notation(self, obj):
        '''
        Method to add new notation. Use this rather than adding directly so new classes can be added automatically
        without needing to know which list to add it to in the main code.
        :param obj: the object to add
        :return: None
        '''
        add = True
        wrap_notation = [
            Arpeggiate,
            NonArpeggiate,
            Slide,
            Glissando,
            mark.Caesura,
            mark.BreathMark,
            GraceNote]
        # method to handle addition of notation: done here to avoid repetitive
        # code in main parser
        if isinstance(obj, ornaments.Tremolo) or isinstance(obj, Tuplet):
            if isinstance(obj, ornaments.Tremolo):
                options = {1: 2, 2: 4, 3: 8}
                if hasattr(obj, "value"):
                    self.trem_length = options[obj.value]
            if hasattr(obj, "type"):
                if isinstance(obj, ornaments.Tremolo) and obj.type != "single":
                    self.trem_length *= 2
                if obj.type == "stop":
                    self.closing_notation.append(obj)
                else:
                    self.prenotation.append(obj)
                return
            else:
                self.prenotation.append(obj)
                return
        if type(obj) in wrap_notation:
            if type(obj) == Slide and not hasattr(obj, "lineType"):
                self.postnotation.append(obj)
                return
            else:
                self.wrap_notation.append(obj)
                return
        if hasattr(obj, "type") and len(self.postnotation) > 0:
            duplicate_check = [
                True for thing in self.postnotation if hasattr(
                    thing,
                    "type") and thing.type == obj.type]
            if len(duplicate_check) > 0:
                add = False
        if len(self.postnotation) == 0 or add:
            self.postnotation.append(obj)

    def set_type(self, vtype):
        '''
        Sets the type, i.e duration of the note. Types are given as keys inside options
        :param vtype: str - see keys in options for full list
        :return: None, side effects modifying the class
        '''
        self.val_type = vtype
        options = {
            "128th": 128,
            "64th": 64,
            "32nd": 32,
            "16th": 16,
            "eighth": 8,
            "quarter": 4,
            "half": 2,
            "whole": 1,
            "h": 8,
            "long": "\\longa",
            "breve": "\\breve"}
        if vtype in options:
            self.duration = options[self.val_type]

    def check_divisions(self, measure_div):
        '''
        Method which is called from voice/measure to update the divisions for each note which are stored at
        measure level, but needed at lilypond time to figure out lilypond notation
        :param measure_div: number of divisions per note. Indicator of how big or small a quarter note is
        :return: None, side effect
        '''
        if hasattr(self, "val_type"):
            self.divisions = 1
        else:
            self.divisions = measure_div

    def __str__(self):
        if hasattr(self, "divisions") and hasattr(self, "duration"):
            self.duration = self.duration / self.divisions
        st = baseclass.Base.__str__(self)
        return st

    def add_dot(self):
        self.dots += 1

    def get_pre_notation_as_lilypond(self):
        '''
        Fetches all notation to come before the note as a lilypond string
        :return: str
        '''
        val = ""
        if hasattr(self, "chord"):
            if self.chord == "start":
                val += "<"
        if hasattr(self, "grace"):
            val += self.grace.to_lily() + " "
        tuplet = self.search(Tuplet, 1)
        if tuplet is None and hasattr(self, "timeMod") and self.timeMod.first:
            val += "\once \override TupletBracket.bracket-visibility = ##f\n"
            val += "\omit TupletNumber\n"
            val += "\\tuplet " + self.timeMod.to_lily() + " {"
        for item in self.prenotation:
            lilystring = item.to_lily()
            if isinstance(item, Tuplet):
                if hasattr(self, "timeMod"):
                    lilystring += " " + self.timeMod.to_lily()
                    lilystring += " {"

            if isinstance(item, ornaments.Tremolo):
                if not hasattr(self, "trem_length"):
                    self.trem_length = lilystring[1]
                    lilystring = lilystring[0]
            val += lilystring

        return val

    def get_beams(self):
        if hasattr(self, "beams"):
            return self.beams

    def get_lily_duration(self):
        """
        method to calculate duration of note in lilypond duration style
        :return:
        """
        value = ""
        if not hasattr(self, "val_type"):
            if hasattr(self, "duration") and self.duration is not None:
                value = (self.duration / self.divisions)
                value = (1 / value)
                value *= 4

                if value >= 1:
                    if math.ceil(value) == value:
                        if hasattr(self, "trem_length"):
                            value *= self.trem_length
                        value = int(value)

                    else:
                        rounded = math.ceil(value)
                        if hasattr(self, "trem_length"):
                            rounded *= self.trem_length
                        value = int(rounded)
                else:
                    if value == 0.5:
                        value = "\\breve"
                    if value == 0.25:
                        value = "\longa"
        else:
            value = self.duration
            if hasattr(self, "trem_length"):
                value *= self.trem_length
        if type(value) is not str:
            value = int(value)
        if value != "":
            value = str(value)
        return value

    def add_beam(self, id, beam):
        if not hasattr(self, "beams"):
            self.beams = {}
        result = [True for b in self.beams if self.beams[b].type == beam.type]
        if len(result) < 1:
            self.beams[id] = beam

    def add_tie(self, type):
        add = True
        for tie in self.ties:
            if tie.type == type:
                add = False
                break
        if add:
            self.ties.append(Tie(type))

    def to_lily(self):
        val = ""
        value = ""
        if hasattr(self, "print") and not self.print:
            val += "\n\\hideNotes\n"
        val += self.get_pre_notation_as_lilypond()
        if hasattr(self, "pitch") and not self.rest:
            val += self.pitch.to_lily()

        if self.rest:
            if not hasattr(self, "MeasureRest") or not self.MeasureRest:
                val += "r"
        if hasattr(
                self,
                "duration") and (
                not hasattr(
                self,
                "MeasureRest") or not self.MeasureRest):
            if not hasattr(self, "chord"):
                val += self.get_lily_duration()
                for dot in range(self.dots):
                    val += "."
        val += self.handle_post_lilies()
        value = self.lily_wrap(val)
        if hasattr(self, "print"):
            value += "\n\\unHideNotes"
        if hasattr(self, "close_timemod") and self.close_timemod:
            value += "}"
        return value

    def lily_wrap(self, value):
        '''
        Method to fetch lilypond representation of wrap_notation
        :param value: current lilypond string to wrap
        :return: updated lilypond string
        '''
        prefixes = ""
        wrapped_notation_lilystrings = [
            wrap.to_lily() for wrap in self.wrap_notation]
        if hasattr(self, "notehead"):
            wrapped_notation_lilystrings.append(self.notehead.to_lily())

        prefixes += "".join([wrapper[0] +
                             " " for wrapper in wrapped_notation_lilystrings if wrapper is not None and len(wrapper) > 1])
        prefixes_and_current = prefixes + value
        postfixes = "".join(
            [wrapper[-1] for wrapper in wrapped_notation_lilystrings if wrapper is not None and len(wrapper) > 0])
        lilystring = prefixes_and_current + postfixes
        return lilystring

    def handle_post_lilies(self):
        val = ""
        if hasattr(self, "chord") and self.chord == "stop":
            val += ">"
            val += self.get_lily_duration()
            for dot in range(self.dots):
                val += "."
        if not hasattr(self, "chord") or self.chord == "stop":
            if hasattr(
                self,
                "beams") and (
                not hasattr(
                    self,
                    "autoBeam") or not self.autoBeam):
                val += "".join([self.beams[beam].to_lily()
                                for beam in self.beams])
            if hasattr(self, "slurs"):
                val += "".join([slur.to_lily() for slur in self.slurs])
            val += "".join([tie.to_lily() for tie in self.ties])
        val += "".join([value.to_lily()
                        for value in self.postnotation if type(value.to_lily()) is str])
        val += "".join([value.to_lily()[0] for value in self.postnotation if type(
            value.to_lily()) is list and len(value.to_lily()) > 0])

        return val

    def search(self, cls_type, list_id=-1):
        '''
        Method which looks for a particular class type in a particular list
        :param cls_type: the type of object to find
        :param list_id: the list it resides in
        :return: the first object of cls_type, or None
        '''
        options = {
            "pre": self.prenotation,
            "post": self.postnotation,
            "wrap": self.wrap_notation}
        if list_id in options:
            for item in options[list_id]:
                if type(item) == cls_type:
                    return item
        else:
            for item in self.prenotation:
                if type(item) == cls_type:
                    return item
            for item in self.wrap_notation:
                if item.__class__.__name__ == cls_type.__name__:
                    return item
                else:
                    print(item.__class__.__name__, cls_type.__name__)
            for item in self.postnotation:
                if type(item) == cls_type:
                    return item


class Tuplet(baseclass.Base):

    """
    Tuplet class.

    Optional inputs:
        type: either start or stop. Represents that this is either the first or last tuplet in the group.
        bracket: bool, indicating whether or not to bracket the tuplets.
    """

    def __init__(self, **kwargs):
        if "type" in kwargs:
            if kwargs["type"] is not None:
                self.type = kwargs["type"]
        if "bracket" in kwargs:
            if kwargs["bracket"] is not None:
                self.bracket = kwargs["bracket"]
        super().__init__()

    def toLily(self):
        val = ""
        if hasattr(self, "bracket"):
            if self.bracket:
                val += "\once \override TupletBracket.bracket-visibility = ##t\n"
            else:
                val += "\once \override TupletBracket.bracket-visibility = ##f\n"
        val += "\\tuplet"
        val = val
        if hasattr(self, "type"):
            if self.type == "stop":
                val = "}"
        return val


class GraceNote(baseclass.Base):

    """
    Gracenotes.

    Optional inputs:
        slash: bool - indicates whether or not the gracenote should be slashed
        first: bool - indicates whether or not this is the first gracenote

    attributes:
        last: bool - indicates whether or not this is the last gracenote in a sequence of gracenotes.
    """

    def __init__(self, **kwargs):
        if "slash" in kwargs:
            self.slash = kwargs["slash"]
        if "first" in kwargs and kwargs["first"] is not None:
            self.first = kwargs["first"]
        super().__init__()

    def to_lily(self):
        val = "\grace"
        ending = ""
        if hasattr(self, "slash") and self.slash:
            val = "\slashedGrace"
        if hasattr(self, "first") and self.first:
            val += " {"
        else:
            val = ""
        if hasattr(self, "last") and self.last:
            ending = " }"
            if not hasattr(self, "first") or not self.first:
                return ending
        return [val, ending]


class TimeModifier(baseclass.Base):

    """
    Class representing a time mod: these sometimes appear in music xml where there are tuplets.

    Optional inputs:
        first: bool - indicates this is the first tuplet
        normal: what the note would normally split into
        actual: the modifier to actually use.
    """

    def __init__(self, **kwargs):
        super().__init__()
        self.first = False
        if "first" in kwargs and kwargs["first"] is not None:
            self.first = kwargs["first"]
        if "normal" in kwargs:
            self.normal = kwargs["normal"]
        if "actual" in kwargs:
            self.actual = kwargs["actual"]

    def toLily(self):
        val = ""
        if hasattr(self, "actual"):
            val += str(self.actual)
        val += "/"
        if hasattr(self, "normal"):
            val += str(self.normal)
        return val


class Arpeggiate(baseclass.Base):

    """
    Arpeggiate class

    Optional inputs:
        direction: direction the arrow head of the arpeggiate should put. Generally up or down I think
        type: whether this is start/stop/none. None indicates it's somewhere in the middle.

    """

    def __init__(self, **kwargs):
        self.wrapped = True
        super().__init__()
        if "direction" in kwargs:
            self.direction = kwargs["direction"]
        if "type" in kwargs:
            self.type = kwargs["type"]
        else:
            self.type = "none"

    def to_lily(self):
        var = "\\arpeggio"
        if not hasattr(self, "direction") or self.direction is None:
            var += "Normal"
        else:
            var += "Arrow" + self.direction.capitalize()
        if self.type == "start":
            return [var, ""]
        if self.type == "stop":
            return ["", "\\arpeggio"]
        if self.type == "none":
            return [""]


class Slide(baseclass.Base):

    """
    Optional Inputs:
        type: the type of gliss, i.e start or stop
        lineType: style of line to use
        number: something that comes in from MusicXML but isn't actually used at min.
    """

    def __init__(self, **kwargs):
        self.wrapped = True
        super().__init__()
        if "type" in kwargs:
            if kwargs["type"] is not None:
                self.type = kwargs["type"]
        if "lineType" in kwargs:
            if kwargs["lineType"] is not None:
                self.lineType = kwargs["lineType"]
        if "number" in kwargs:
            if kwargs["number"] is not None:
                self.number = kwargs["number"]

    def to_lily(self):
        val = ""
        gliss = "\glissando"
        values = []
        if hasattr(self, "lineType"):
            if self.lineType == "wavy":
                val += "\override Glissando.style = #'zigzag"
                values.append(val)
        if hasattr(self, "type"):
            if self.type == "stop":
                values = []
            else:
                values.append(gliss)
        else:
            values.append(gliss)
        return values


class Glissando(Slide):

    """
    A glissando - like a slide, but it really only comes in "wavy" type so lineType is completely ignored.
    """

    def to_lily(self):
        self.lineType = "wavy"
        vals = Slide.to_lily(self)
        return vals


class NonArpeggiate(Arpeggiate):

    def __init__(self, **kwargs):

        Arpeggiate.__init__(self)
        if "type" in kwargs:
            self.type = kwargs["type"]

    def to_lily(self):
        if self.type == "start":
            return ["\\arpeggioBracket", ""]
        if self.type == "stop":
            return ["", "\\arpeggio"]
        if self.type == "none":
            return [""]


class Beam(Stem):

    """
    Class representing beam information. Normally this is automatic, but it comes in from MusicXML anyway
    so may be useful at some stage.

    # Optional input
        - type - indicates whether this is a starting, continuing or ending beam.
    """

    def to_lily(self):
        val = ""
        if hasattr(self, "type"):
            if self.type == "begin":
                val = "["
            elif self.type == "end":
                val = "]"
        return val
