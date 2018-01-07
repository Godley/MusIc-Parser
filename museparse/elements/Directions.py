import string
import random

from museparse.classes.ObjectHierarchy.ItemClasses import BaseClass


class Text(BaseClass.Base):

    """
    A class representing any kind of text


    # Optional inputs

        - font: the font to use. If this isn't in the list of fonts in lilypond, a random one will be picked.

        - size: font size to use

        - text: the actual text to display
    """

    def __init__(self, **kwargs):
        BaseClass.Base.__init__(self)
        if "font" in kwargs and kwargs["font"] is not None:
            self.font = kwargs["font"]
        if "size" in kwargs and kwargs["size"] is not None:
            self.size = kwargs["size"]
        if "text" in kwargs and kwargs["text"] is not None:
            self.text = kwargs["text"]
        else:
            self.text = ""

    def get(self):
        """
        method to fetch all contents as a list

        :return: list
        """
        ret_list = []
        if hasattr(self, "font"):
            ret_list.append(self.font)
        if hasattr(self, "size"):
            ret_list.append(self.size)
        if hasattr(self, "text"):
            ret_list.append(self.text)
        return ret_list

    def to_lily(self):
        '''
        Method which converts the object instance and its attributes to a string of lilypond code

        :return: str of lilypond code
        '''

        lilystring = ""
        if hasattr(self, "size"):
            try:
                size = float(self.size)
                lilystring += "\\abs-fontsize #" + str(self.size) + " "
            except:
                lilystring += "\\" + str(self.size) + " "
        if hasattr(self, "font"):
            fonts_available = ["sans", "typewriter", "roman"]
            if self.font in fonts_available:
                lilystring += "\\" + self.font + " "
            else:
                rand = random.Random()
                selected = rand.choice(fonts_available)
                lilystring += "\\" + selected + " "
        valid = False
        for char in self.text:
            if char in string.ascii_letters or char in [
                    "0",
                    "1",
                    "2",
                    "3",
                    "4",
                    "5",
                    "6",
                    "7",
                    "8",
                    "9"]:
                if not hasattr(self, "noquotes"):
                    lilystring += "\""
                lilystring += self.text
                if not hasattr(self, "noquotes"):
                    lilystring += "\" "
                valid = True
                break
            else:
                valid = False
        if not valid:
            lilystring = ""
        return lilystring


class CreditText(Text):

    """
    Class which represents credits - anything which is to go at the bottom of the page, like copyrights,
    authors etc. Essentially the same as text except it can be positioned


    # Optional inputs

        - x: the x position of the text

        - y: the y position of the text

        - justify: left/right

        - valign: vertical alignment - top/bottom

        - page: unused, but the page to put this text on
    """

    def __init__(self, **kwargs):
        font = None
        size = None
        text = None
        if "font" in kwargs:
            font = kwargs["font"]
        if "size" in kwargs:
            size = kwargs["size"]
        if "text" in kwargs:
            text = kwargs["text"]
        if "x" in kwargs:
            if kwargs["x"] is not None:
                self.x = kwargs["x"]
        if "y" in kwargs:
            if kwargs["y"] is not None:
                self.y = kwargs["y"]
        if "size" in kwargs:
            if kwargs["size"] is not None:
                self.size = kwargs["size"]
        if "justify" in kwargs:
            if kwargs["justify"] is not None:
                self.justify = kwargs["justify"]
        if "valign" in kwargs:
            if kwargs["valign"] is not None:
                self.valign = kwargs["valign"]
        if "page" in kwargs:
            if kwargs["page"] is not None:
                self.page = kwargs["page"]
        Text.__init__(self, font=font, size=size, text=text)

    def to_lily(self):
        lily = ""
        if hasattr(self, "justify"):
            options = {
                "right": "\\fill-line {\n\\null \n\override #'(baseline-skip . 4)\n\override #'(line-width . 40) {",
                "center": "\\fill-line { \n \\center-column {\n"}
            if self.justify in options:
                lily += options[self.justify]
        if hasattr(self, "valign"):
            option = {"top": "UP", "bottom": "DOWN"}
            lily += "\general-align #Y #" + option[self.valign] + "\n "
        lily += Text.to_lily(self)
        if hasattr(self, "justify"):
            options = {"right": "\n}\n\t}\n\\null\\null", "center": "\n}\n}"}
            if self.justify in options:
                lily += options[self.justify]
        return lily


class Lyric(Text):

    """
    Text class representing lyrics. Unused because needs readjustment in order to fit lyrics into Lilypond's output.
    Essentially the same as text but 1 additional input


    # Optional input

        - syllabic: whether this lyric is meant to fit syllables to each diff note
    """

    def __init__(self, **kwargs):
        font = None
        text = None
        size = None
        if "font" in kwargs:
            font = kwargs["font"]
        if "text" in kwargs:
            text = kwargs["text"]
        if "size" in kwargs:
            size = kwargs["size"]
        if "syllabic" in kwargs:
            self.syllabic = kwargs["syllabic"]
        Text.__init__(self, text=text, font=font, size=size)


class Direction(Text):

    """
    Class representing directions - see sub classes for what these generally are. This class is used for
    regular text directions such as "andante" or "cantabile"


    # Optional inputs

        - placement: above or below the bar
    """

    def __init__(self, **kwargs):
        text = None
        size = None
        font = None
        if "placement" in kwargs:
            if kwargs["placement"] is not None:
                self.placement = kwargs["placement"]
        if "text" in kwargs:
            text = kwargs["text"]
        if "size" in kwargs:
            size = kwargs["size"]
        if "font" in kwargs:
            font = kwargs["font"]
        Text.__init__(self, text=text, size=size, font=font)

    def to_lily(self):
        textLilyString = Text.to_lily(self)
        symbol = ""
        return_val = " "
        if hasattr(self, "placement"):
            if self.placement == "above":
                symbol = "^"
            if self.placement == "below":
                symbol = "_"
            if self.placement == "none":
                symbol = ""
        else:
            symbol = "^"
        if len(textLilyString) > 0:
            return_val += symbol + "\\markup { " + textLilyString + " }"
        return return_val


class RehearsalMark(Direction):

    """
    Class representing rehearsal marks like A in a box above a bar.

    Same as direction, except that text - generally "A" or "C" is used to figure out which number mark lilypond is expecting.
    """

    def to_lily(self):
        text = " \mark "
        if self.text == "":
            text += "\default"
        else:
            try:
                index = string.ascii_lowercase.index(self.text.lower()) + 1
                text += "#" + str(index)
            except:
                text += "\default"
        return text


class Forward(Direction):

    """
    Probably an unused class - forwards arent what I thought they were.
    """

    def __init__(self, **kwargs):
        text = None
        size = None
        font = None
        placement = None
        if "duration" in kwargs:
            self.duration = kwargs["duration"]
        if "type" in kwargs:
            self.type = kwargs["type"]
        if "placement" in kwargs:
            if kwargs["placement"] is not None:
                placement = kwargs["placement"]
        if "text" in kwargs:
            text = kwargs["text"]
        if "size" in kwargs:
            size = kwargs["size"]
        if "font" in kwargs:
            font = kwargs["font"]
        Direction.__init__(
            self,
            placement=placement,
            text=text,
            size=size,
            font=font)

    def to_lily(self):
        lilystring = "percent repeat"
        return_list = [lilystring]
        if hasattr(self, "duration"):
            if self.duration is None:
                self.duration = 2
            return_list.append(int(self.duration))
        return return_list


class RepeatSign(Direction):

    """
    Class representing coda symbols and DC symbols.
    """

    def __init__(self, **kwargs):
        text = None
        size = None
        font = None
        placement = None
        self.noquotes = True
        if "type" in kwargs:
            if kwargs["type"] is not None:
                self.type = kwargs["type"]
                text = "\musicglyph #\"scripts." + self.type + "\""
        if "placement" in kwargs:
            if kwargs["placement"] is not None:
                self.sym_placement = kwargs["placement"]
        placement = "none"
        if "text" in kwargs:
            text = kwargs["text"]
        if "size" in kwargs:
            size = kwargs["size"]
        if "font" in kwargs:
            font = kwargs["font"]
        Direction.__init__(
            self,
            placement=placement,
            text=text,
            size=size,
            font=font)

    def to_lily(self):
        return " \mark " + Direction.to_lily(self)


class Line(Direction):

    """
    Class representing lines over the bar, such as brackets or braces. Essentially I think this is a stub to be sub classed
    so don't instantiate line on its own without some modification.
    """

    def __init__(self, **kwargs):
        text = None
        size = None
        font = None
        placement = None
        if "placement" in kwargs:
            placement = kwargs["placement"]

        if "text" in kwargs:
            text = kwargs["text"]
        if "size" in kwargs:
            size = kwargs["size"]
        if "font" in kwargs:
            font = kwargs["font"]
        if "type" in kwargs:
            if kwargs["type"] is not None:
                self.type = kwargs["type"]
        Direction.__init__(
            self,
            text=text,
            size=size,
            font=font,
            placement=placement)


class OctaveShift(Line):

    """
    Class representing specifically octave shifts


    # Optional inputs

        - amount: the amount to shift up/down octaves. Int, generally 8 or 15 depending on whether 1 or 2

        - type: type of shift - up/down.

    """

    def __init__(self, **kwargs):
        placement = None
        text = None
        font = None
        size = None
        type = None
        if "amount" in kwargs:
            if kwargs["amount"] is not None:
                self.amount = kwargs["amount"]
        if "placement" in kwargs:
            placement = kwargs["placement"]

        if "text" in kwargs:
            text = kwargs["text"]
        if "size" in kwargs:
            size = kwargs["size"]
        if "font" in kwargs:
            font = kwargs["font"]
        if "type" in kwargs:
            if kwargs["type"] is not None:
                type = kwargs["type"]
        Line.__init__(
            self,
            text=text,
            type=type,
            size=size,
            font=font,
            placement=placement)

    def to_lily(self):
        return_val = "\n\ottava #"
        multiplier = 1
        octave = 0
        if hasattr(self, "type"):
            if self.type == "up":
                return_val += "-"

        if hasattr(self, "amount"):
            if self.amount == 8:
                octave = 1
            if self.amount == 15:
                octave = 2
        else:
            octave = 1

        return_val += str(octave) + "\n"
        if hasattr(self, "type"):
            if self.type == "stop":
                return_val = "\n\ottava #0"
        return return_val


class WavyLine(Line):

    """
    Class representing a wavy line, such as the one used for an extended trill marking
    """

    def to_lily(self):
        if not hasattr(self, "type"):
            text = "\start"
        else:
            text = "\\" + self.type
        return text + "TrillSpan"


class Pedal(Line):

    """
    A piano pedal marker class.


    # Optional inputs

        - line: bool representing whether or not to display a line

        - type: start/stop
    """

    def __init__(self, **kwargs):
        text = None
        size = None
        font = None
        type = None
        placement = None
        if "line" in kwargs:
            if kwargs["line"] is not None:
                self.line = kwargs["line"]
        if "placement" in kwargs:
            placement = kwargs["placement"]
        if "text" in kwargs:
            text = kwargs["text"]
        if "size" in kwargs:
            size = kwargs["size"]
        if "font" in kwargs:
            font = kwargs["font"]
        if "type" in kwargs:
            type = kwargs["type"]
        Line.__init__(
            self,
            type=type,
            text=text,
            size=size,
            font=font,
            placement=placement)

    def to_lily(self):
        return_val = ""
        if (hasattr(self, "type") and self.type != "stop") or not hasattr(
                self, "type"):
            if hasattr(self, "line"):
                if not self.line:
                    return_val += "\n\set Staff.pedalSustainStyle = #'text\n"
        return_val += "\sustain"
        if hasattr(self, "type"):
            if self.type == "stop":
                return_val += "Off\n"
            if self.type == "change":
                return_val += "Off\sustainOn\n"
            elif self.type == "start":
                return_val += "On\n"

        else:
            return_val += "On\n"
        return return_val


class Bracket(Line):

    def __init__(self, **kwargs):
        text = None
        size = None
        font = None
        type = None
        placement = None
        if "number" in kwargs:
            if kwargs["number"] is not None:
                self.number = kwargs["number"]
        if "ltype" in kwargs:
            if kwargs["ltype"] is not None:
                self.lineType = kwargs["ltype"]
        if "elength" in kwargs:
            if kwargs["elength"] is not None:
                self.endLength = kwargs["elength"]
        if "lineEnd" in kwargs:
            if kwargs["lineEnd"] is not None:
                self.lineEnd = kwargs["lineEnd"]
        if "placement" in kwargs:
            placement = kwargs["placement"]
        if "text" in kwargs:
            text = kwargs["text"]
        if "size" in kwargs:
            size = kwargs["size"]
        if "font" in kwargs:
            font = kwargs["font"]
        if "type" in kwargs:
            type = kwargs["type"]
        Line.__init__(
            self,
            type=type,
            text=text,
            size=size,
            font=font,
            placement=placement)

    def to_lily(self):
        lilystring = ""
        style_line = ""
        if hasattr(self, "lineType"):
            if self.lineType == "solid":
                lilystring = "\\override TextSpanner.dash-fraction = 1.0 \n"
            elif self.lineType == "dashed":
                lilystring = "\\override TextSpanner.dash-fraction = 0.5 \n"
        if hasattr(self, "type"):
            if self.type == "stop":
                lilystring = "\n\\stopTextSpan\n"
            elif self.type == "start":
                lilystring = "\n\\startTextSpan\n"
        return lilystring


class Metronome(Direction):

    """
    Class representing a metronome mark, which can be a combination of <note> = <number per minute> and text


    # Optional inputs

        - beat: the beat marker. I.e <beat> = <bpm>

        - min: the number of beats per minute.

        - secondBeat: in place of min, could also have this representing another beat. Like crotchet = quaver

        - text: the text to display with the metronome mark


    attributes:

        - parentheses: this could also be optionally set later to indicate whether or not to put parentheses round the mark.
                        bool.
    """

    def __init__(self, **kwargs):
        size = None
        font = None
        text = None
        if "secondBeat" in kwargs:
            self.secondBeat = kwargs["secondBeat"]
        if "beat" in kwargs:
            self.beat = kwargs["beat"]
        if "min" in kwargs:
            self.min = kwargs["min"]
        if "text" in kwargs:
            if isinstance(kwargs["text"], str):
                text = kwargs["text"]
            elif kwargs["text"] is not None:
                text = kwargs["text"].text
        if "size" in kwargs:
            size = kwargs["text"]
        if "font" in kwargs:
            font = kwargs["font"]
        Text.__init__(self, text=text, size=size, font=font)
        if "parentheses" in kwargs:
            if kwargs["parentheses"] is not None:
                self.parentheses = kwargs["parentheses"]
        else:
            self.parentheses = False

    def to_lily(self):
        return_val = " \\tempo "
        converter = {
            "eighth": 8,
            "quarter": 4,
            "half": 2,
            "whole": 1,
            "long": "longa",
            "breve": "\\breve",
            "32nd": 32}
        if hasattr(self, "parentheses"):
            if self.parentheses and self.text == "" and not hasattr(
                    self,
                    "secondBeat"):
                return_val += "\"\" "
        if self.text != "":
            return_val += "\"" + self.text + "\" "
        if hasattr(self, "beat") and hasattr(self, "min"):
            if self.beat == "long":
                return_val += "\\"
            return_val += str(converter[self.beat]) + "=" + str(self.min)
        elif hasattr(self, "secondBeat") and hasattr(self, "beat"):
            return_val += "\markup {\n\t\concat {\n\t\t"
            if hasattr(self, "parentheses") and self.parentheses:
                return_val += "("
            return_val += "\n\t\t\t\smaller \general-align #Y #DOWN \\note #\""
            return_val += str(
                converter[
                    self.beat]) + "\" #1\n\t\t\t\t\" = \"\n\t\t\t\t\smaller \general-align #Y #DOWN \\note #\""
            return_val += str(converter[self.secondBeat]) + "\" #1\n\t\t"
            if hasattr(self, "parentheses") and self.parentheses:
                return_val += ")"
            return_val += "\n\t}\n}"
        else:
            return_val = ""

        return return_val

    def get_detail(self):
        ret_list = self.get()
        if hasattr(self, "beat"):
            ret_list.append(self.beat)
        if hasattr(self, "min"):
            ret_list.append(self.min)
        return ret_list


class Dynamic(Direction):

    """
    Dynamic marking class


    # Optional inputs

        - mark: the mark to use in the dynamic
    """

    def __init__(self, **kwargs):
        placement = None
        size = None
        font = None
        text = None
        if "mark" in kwargs:
            self.mark = kwargs["mark"]
            text = self.mark
        if "text" in kwargs:
            text = kwargs["text"]

        if "size" in kwargs:
            size = kwargs["size"]

        if "font" in kwargs:
            font = kwargs["font"]
        if "placement" in kwargs:
            placement = kwargs["placement"]

        Direction.__init__(self, placement=placement,
                           font=font,
                           size=size,
                           text=text)

    def to_lily(self):
        return_val = "\\"
        if hasattr(self, "mark") and len(self.mark) < 6:
            special_marks = [
                "ppppp",
                "pppp",
                "ppp",
                "pp",
                "p",
                "mp",
                "mf",
                "f",
                "ff",
                "fff",
                "ffff",
                "fffff",
                "fp",
                "sf",
                "sff",
                "sp",
                "spp",
                "sfz",
                "rfz"]
            if self.mark in special_marks:
                return_val += self.mark
            else:
                return_val = ""
        else:
            return_val = ""
        return return_val


class Wedge(Dynamic):

    """
    Wedge - i.e crescendo line or decrescendo line


    # Optional inputs

        - type: crescendo/diminuendo/stop. In Lilypond stop is an option because every wedge must end somewhere,
                and this gives an indication to stop the wedge at x position.
    """

    def __init__(self, **kwargs):
        placement = None
        self.type = None
        if "placement" in kwargs:
            placement = kwargs["placement"]
        if "type" in kwargs:
            self.type = kwargs["type"]

        Dynamic.__init__(self, placement=placement, text=self.type)

    def to_lily(self):
        return_val = "\\"
        if hasattr(self, "type"):
            if self.type == "crescendo":
                return_val += "<"
            if self.type == "diminuendo":
                return_val += ">"
            if self.type == "stop":
                return_val += "!"

        return return_val


class Slur(Direction):

    """
    Slur class


    # Optional inputs

        - type: start/stop
    """

    def __init__(self, **kwargs):
        placement = None
        size = None
        font = None
        if "size" in kwargs:
            size = kwargs["size"]

        if "font" in kwargs:
            font = kwargs["font"]
        if "placement" in kwargs:
            placement = kwargs["placement"]

        if "type" in kwargs:
            if kwargs["type"] is not None:
                self.type = kwargs["type"]

        Direction.__init__(self, placement=placement,
                           font=font,
                           size=size)

    def to_lily(self):

        return_val = ""
        if hasattr(self, "type"):
            if self.type == "start":
                return_val += "("
            if self.type == "stop":
                return_val += ")"
        return return_val
