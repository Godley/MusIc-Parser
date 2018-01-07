
majors = {-
          7: "Cflat", -
          6: "Gflat", -
          5: "Dflat", -
          4: "Aflat", -
          3: "Eflat", -
          2: "Bflat", -
          1: "F", 0: "C", 1: "G", 2: "D", 3: "A", 4: "E", 5: "B", 6: "Fsharp", 7: "Csharp"}
'''dictionary of all key signature names in the major mode, indexed by their number of fifths'''
minors = {-7: "Aflat", -6: "Eflat", -5: "Bflat", -4: "F", -3: "C", -2: "G", -1: "D",
          0: "A", 1: "E", 2: "B", 3: "Fsharp", 4: "Csharp", 5: "Gsharp", 6: "Dsharp", 7: "Asharp"}
'''dictionary of all key signature names in the minor mode, indexed by their number of fifths'''


class Key(object):

    """
    key signature class


    # Optional inputs

            - fifths: the number of fifths in the key sig. int

            - mode: major/minor
    """

    def __init__(self, **kwargs):
        if "fifths" in kwargs:
            self.fifths = kwargs["fifths"]
        if "mode" in kwargs:
            self.mode = kwargs["mode"]

    def __str__(self):
        if hasattr(self, "fifths"):
            if hasattr(self, "mode"):
                if self.mode == "major":
                    return majors[self.fifths] + " major"
                if self.mode == "minor":
                    return minors[self.fifths] + " minor"

    def to_lily(self):
        val = "\key"
        if hasattr(self, "fifths"):
            if hasattr(self, "mode"):
                keyname = ""
                if self.mode == "major":
                    if self.fifths in majors:
                        keyname = majors[self.fifths].lower()
                if self.mode == "minor":
                    if self.fifths in minors:
                        keyname = minors[self.fifths].lower()
                if len(keyname) > 1:
                    symbol = keyname[1:len(keyname)]
                    if symbol == "flat":
                        keyname = keyname[0] + "es"
                    if symbol == "sharp":
                        keyname = keyname[0] + "is"
                val += " " + keyname
                val += " \\" + self.mode
            else:
                val = ""
        else:
            val = ""
        return val
