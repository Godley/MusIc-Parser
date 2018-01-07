# Lots of classes relating to notation. fairly obvious what they are and
# do based on their class name


class Notation(object):

    """
    Notation parent class. Not generally instantiated anywhere

    # Optional inputs
        placement: above/below I think. Not used.
        symbol: symbol to display.
    """

    def __init__(self, **kwargs):
        if "placement" in kwargs:
            self.placement = kwargs["placement"]
        if "symbol" in kwargs:
            self.symbol = kwargs["symbol"]

    def __str__(self):
        str_val = ""
        if hasattr(self, "placement") and self.placement is not None:
            str_val += self.placement
        if hasattr(self, "symbol") and self.symbol is not None:
            str_val += self.symbol
        return str_val

    def to_lily(self):
        '''
        Method which converts the object instance and its attributes to a string of lilypond code
        :return: str of lilypond code
        '''
        return "\\"


class Accent(Notation):

    def __init__(self, **kwargs):
        placement = None
        if "placement" in kwargs:
            placement = kwargs["placement"]
        Notation.__init__(self, placement=placement, symbol="-")

    def to_lily(self):
        val = Notation.to_lily(self)
        val += "accent "
        return val


class StrongAccent(Notation):

    def __init__(self, **kwargs):
        placement = None
        if "placement" in kwargs:
            placement = kwargs["placement"]

        symbol = ""
        if "type" in kwargs:
            self.type = kwargs["type"]
            if self.type == "up":
                symbol = "^"
            else:
                symbol = "V"
        Notation.__init__(self, placement=placement, symbol=symbol)

    def to_lily(self):
        val = Notation.to_lily(self)
        val += "marcato "
        return val


class Staccato(Notation):

    def __init__(self, **kwargs):
        placement = None
        if "placement" in kwargs:
            placement = kwargs["placement"]

        symbol = "."
        Notation.__init__(self, placement=placement, symbol=symbol)

    def to_lily(self):
        val = Notation.to_lily(self)
        val += "staccato "
        return val


class Staccatissimo(Notation):

    def __init__(self, **kwargs):
        placement = None
        if "placement" in kwargs:
            placement = kwargs["placement"]

        symbol = "triangle"
        Notation.__init__(self, placement=placement, symbol=symbol)

    def to_lily(self):
        val = Notation.to_lily(self)
        val += "staccatissimo "
        return val


class Tenuto(Notation):

    def __init__(self, **kwargs):
        placement = None
        if "placement" in kwargs:
            placement = kwargs["placement"]

        symbol = "line"
        Notation.__init__(self, placement=placement, symbol=symbol)

    def to_lily(self):
        val = Notation.to_lily(self)
        val += "tenuto "
        return val


class DetachedLegato(Notation):

    def __init__(self, **kwargs):
        placement = None
        if "placement" in kwargs:
            placement = kwargs["placement"]

        symbol = "lineDot"
        Notation.__init__(self, placement=placement, symbol=symbol)

    def to_lily(self):
        val = Notation.to_lily(self)
        val += "portato "
        return val


class Fermata(Notation):

    def __init__(self, **kwargs):
        placement = None
        if "placement" in kwargs:
            placement = kwargs["placement"]

        if "type" in kwargs:
            self.type = kwargs["type"]

        symbol = "fermata"
        if "symbol" in kwargs:
            symbol = kwargs["symbol"]
        super().__init__(placement=placement, symbol=symbol)

    def to_lily(self):
        val = Notation.to_lily(self)
        if hasattr(self, "symbol"):
            if self.symbol != "fermata":
                if self.symbol == "angled":
                    val += "short"
                if self.symbol == "square":
                    val += "long"
                if self.symbol == "squared":
                    val += "verylong"
        val += "fermata "
        return val


class BreathMark(Notation):

    def to_lily(self):
        val = Notation.to_lily(self)
        val += "breathe "
        styling = "\override Staff.BreathingSign.text = \markup { \musicglyph #\"scripts.rvarcomma\" }"
        return [styling, val]


class Caesura(BreathMark):

    def to_lily(self):
        lstring = BreathMark.to_lily(self)
        styling = "\override BreathingSign.text = \markup { \musicglyph #\"scripts.caesura.curved\" }"
        return [styling, lstring[1]]


class Technique(Notation):

    def __init__(self, **kwargs):
        placement = None
        size = None
        font = None
        symbol = None
        text = None
        if "type" in kwargs:
            self.type = kwargs["type"]
        if "symbol" in kwargs:
            symbol = kwargs["symbol"]
        if "placement" in kwargs:
            placement = kwargs["placement"]
        super().__init__(placement=placement,
                          symbol=symbol)

    def to_lily(self):
        val = super().to_lily()
        if hasattr(self, "type"):
            if self.type != "fingering" and self.type != "pluck" and self.type != "string":
                splitter = self.type.split("-")
                joined = "".join(splitter)
                val += joined + " "
            else:
                if self.type == "fingering":
                    if hasattr(self, "symbol"):
                        val = "-" + str(self.symbol)
                if self.type == "string":
                    if hasattr(self, "symbol"):
                        val = "\\" + str(self.symbol)
                elif self.type != "fingering":
                    val = "_\\markup { "
                    if self.symbol is not None:
                        val += self.symbol
                    val += " }"
        return val


class Bend(Notation):

    def __init__(self, **kwargs):
        if "value" in kwargs:
            self.value = kwargs["value"]
        super().__init__(**kwargs)

    def to_lily(self):
        val = "\\bendAfter #"
        if hasattr(self, "value"):
            if self.value > 0:
                val += "+"
            if self.value < 0:
                val += "-"
            val += str(self.value)

        return val
