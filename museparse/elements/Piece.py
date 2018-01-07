class Piece(object):

    def __init__(self):
        self.Parts = {}

    def __str__(self):
        st = ""
        if hasattr(self, "meta"):
            st += str(self.meta)
        for key in sorted(self.Parts.keys()):
            st += "\n"
            st += "Part: "
            st += key
            st += "\n Details: "
            st += str(self.Parts[key])
        return st

    def to_lily(self):
        lilystring = ""
        if hasattr(self, "meta"):
            lilystring += "\n" + self.meta.to_lily()
        return lilystring
