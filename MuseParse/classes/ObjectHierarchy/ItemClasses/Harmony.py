from MuseParse.classes.ObjectHierarchy.ItemClasses import BaseClass, Note


class Harmony(BaseClass.Base):
    """
    Class representing a harmony chord chart for guitarists. Not currently implemented 100% correct in lilypond notation

    For info on the optional inputs root/kind/bass/frame please refer to the MusicXML documentation, as I don't 100% understand
    this myself. Class representations for each are beneath this class.
    """
    def __init__(self, **kwargs):
        self.degrees = []
        if "root" in kwargs:
            if kwargs["root"] is not None:
                self.root = kwargs["root"]
        if "kind" in kwargs:
            if kwargs["kind"] is not None:
                self.kind = kwargs["kind"]
        if "bass" in kwargs:
            if kwargs["bass"] is not None:
                self.bass = kwargs["bass"]
        if "degrees" in kwargs:
            self.degrees = kwargs["degrees"]
        if "frame" in kwargs:
            self.frame = kwargs["frame"]
        BaseClass.Base.__init__(self)

    def toLily(self):
        val = "\chords {"
        if hasattr(self, "root"):
            val += "\n\r" + self.root
        if hasattr(
                self,
                "bass") or len(
                self.degrees) > 0 or hasattr(
                self,
                "kind"):
            val += "\n\r:"
        if hasattr(self, "degrees"):
            for degree in self.degrees:
                if hasattr(self, "kind"):
                    if self.kind.parenthesis:
                        val += "("
                val += degree.toLily()
                if hasattr(self, "kind"):
                    if self.kind.parenthesis:
                        val += ")"
        if hasattr(self, "bass"):
            val += "/" + self.bass
        val += "\n\r}"
        if hasattr(self, "frame"):
            return_val = []
            return_val.append(val)
            return_val.append(self.frame.toLily())
            val = return_val
        return val


class Frame(BaseClass.Base):

    def __init__(self, **kwargs):
        if "strings" in kwargs:
            if kwargs["strings"] is not None:
                self.strings = kwargs["strings"]
            else:
                self.strings = 6
        if "frets" in kwargs:
            if kwargs["frets"] is not None:
                self.frets = kwargs["frets"]
        self.notes = {}
        if "notes" in kwargs:
            self.notes = kwargs["notes"]
        BaseClass.Base.__init__(self)

    def toLily(self):
        val = ""
        val += "^\markup {\n\r\\fret-diagram #\""
        if hasattr(self, "frets"):
            val += "h:" + str(self.frets) + ";"
        if hasattr(self, "strings"):
            val += "w:" + str(self.strings) + ";"
            value = self.strings
            while value > 0:
                val += str(value)
                if value in self.notes:
                    val += self.notes[value].toLily()
                    try:
                        fret = int(val[-2])
                        if val[-1] == "-":
                            barres = [str(key) for key in self.notes.keys()
                                      if hasattr(self.notes[key], "barre")
                                      and self.notes[key].barre == "stop"
                                      and self.notes[key].fret == fret]
                            if len(barres) > 0:
                                val += "-".join(barres)

                    except:
                        pass

                else:
                    val += "-o"
                val += ";"
                value -= 1

        val += "\"\n}"
        return val


class FrameNote(BaseClass.Base):

    def __init__(self, **kwargs):
        if "string" in kwargs:
            self.string = kwargs["string"]
        if "fret" in kwargs:
            self.fret = kwargs["fret"]
        BaseClass.Base.__init__(self)

    def toLily(self):
        val = ""
        if hasattr(self, "string"):
            val += str(self.string)
        val += "-"
        if hasattr(self, "fret"):
            val += str(self.fret)
        if hasattr(self, "barre"):
            if self.barre == "start":
                val += "-"
        return val


class Kind(BaseClass.Base):

    def __init__(self, **kwargs):
        if "value" in kwargs:
            if kwargs["value"] is not None:
                self.value = kwargs["value"]
        if "halign" in kwargs:
            if kwargs["halign"] is not None:
                self.halign = kwargs["halign"]
        if "text" in kwargs:
            if kwargs["text"] is not None:
                self.text = kwargs["text"]
        if "parenthesis" in kwargs:
            if kwargs["parenthesis"] is not None:
                self.parenthesis = kwargs["parenthesis"]
        BaseClass.Base.__init__(self)

    def toLily(self):
        val = ""
        if hasattr(self, "parenthesis"):
            if self.parenthesis:
                val += "("
        if not hasattr(self, "text"):
            if hasattr(self, "value"):
                val += str(self.value)
        else:
            val += self.text
        if hasattr(self, "parenthesis"):
            if self.parenthesis:
                val += ")"
        return val


class Degree(BaseClass.Base):

    def __init__(self, **kwargs):
        if "alter" in kwargs and kwargs["alter"] is not None:
            self.alter = kwargs["alter"]
        if "value" in kwargs and kwargs["value"] is not None:
            self.value = kwargs["value"]
        if "type" in kwargs and kwargs["type"] is not None:
            self.type = kwargs["type"]
        BaseClass.Base.__init__(self)

    def toLily(self):
        val = ""
        if hasattr(self, "type"):
            if self.type == "subtract":
                val += "no "
            if self.type == "add":
                val += "add "
            if self.type == "alter":
                val += "#"
        if hasattr(self, "alter"):
            pass
        if hasattr(self, "value"):
            val += str(self.value)

        return val


class harmonyPitch(Note.Pitch):
    pass
