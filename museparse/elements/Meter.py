class Meter(object):

    """
    Class representing time signatures/meter markings.

    # Optional inputs

            - beats: number of beats in every bar

            - type: type of beats in every bar

            - style: indicator of how it should be displayed. Used for single digit meters using value "single-number"
    """

    def __init__(self, **kwargs):
        if "beats" in kwargs:
            self.beats = kwargs["beats"]
        if "type" in kwargs:
            self.type = kwargs["type"]
        if "style" in kwargs and kwargs["style"] is not None:
            self.style = kwargs["style"]

    def __str__(self):
        return str(self.beats) + "/" + str(self.type)

    def to_lily(self):
        val = ""
        if hasattr(self, "style") and self.style == "single-number":
            val += "\n\once \override Staff.TimeSignature.style = #'single-digit\n"
        val += "\\time"
        if hasattr(self, "beats"):
            val += " " + str(self.beats)
            if hasattr(self, "type"):
                val += "/" + str(self.type)
            else:
                if self.beats <= 4:
                    val += "/4"
                elif 4 < self.beats <= 8:
                    val += "/8"
        elif not hasattr(self, "type"):
            val += " 4/4"
        else:
            val += " " + str(self.type) + "/" + str(self.type)

        return val
