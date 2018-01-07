from museparse.elements import baseclass


class Meta(baseclass.Base):

    """
    Class which holds information about the piece.


    # Optional inputs

    - title: name of the piece

    - composer

    - copyright: company or tag line who owns the copyright
    """

    def __init__(self, **kwargs):
        super().__init__()
        if "title" in kwargs:
            if kwargs["title"] is not None:
                self.title = kwargs["title"]
        if "composer" in kwargs:
            if kwargs["composer"] is not None:
                self.composer = kwargs["composer"]
        if "copyright" in kwargs:
            if kwargs["copyright"] is not None:
                self.copyright = kwargs["copyright"]

    def escape_quotes(self, value):
        list_of_string = list(value)
        output = []
        for item in list_of_string:
            if item == "\"":
                output.append("\\")
            output.append(item)
        return "".join(output)

    def to_lily(self):
        val = "\header {\n"
        if hasattr(self, "title") and self.title is not None:
            val += "title = \"" + self.escape_quotes(self.title) + "\"\n"
        if hasattr(self, "composer") and self.composer is not None:
            val += "composer = \"" + self.escape_quotes(self.composer) + "\"\n"
        if hasattr(self, "copyright"):
            val += "tagline = \"" + self.escape_quotes(self.copyright) + "\""
        val += "\n}"
        if hasattr(self, "pageNum"):
            if self.pageNum:
                val += "\n \paper {\n print-page-number = True \n}\n\n"
        if hasattr(self, "credits"):
            val += "\\markuplist {"
            for credit in self.credits:
                val += "\n\\vspace #0.5\n"
                val += "\n" + credit.to_lily()
            val += " }"

        return val

    def add_credit(self, credit):
        if not hasattr(self, "credits"):
            self.credits = []
        self.credits.append(credit)
