import os
import subprocess
import sys
from museparse import exceptions


class LilypondRenderer(object):
    """
    Class which handles output of a PieceTree class, or in fact, any other hierarchy where each object has its own toLily method.

    # Required Inputs

        - piece_obj: the hierarchy of objects representing the piece in memory

        - fname: the location of the original file being represented. Extension not important, but should be there.

    # Optional Inputs

        - lyscript: the location of the script which should be ran as the first argument in the command to execute lilypond. If none is given, the system will take the default script according to the command line instructions on the lilypond website.
    """

    def __init__(
            self,
            piece_obj,
            fname,
            lyscript=""):
        self.piece_obj = piece_obj
        self.file = fname
        self.lyfile = self.file.split(".")[0] + ".ly"
        self.pdf = self.file.split(".")[0] + ".pdf"
        self.folder = os.path.join(*os.path.split(self.file)[:-1])

        self.default = "lilypond"
        if lyscript != "" and lyscript is not None:
            self.lily_script = lyscript
        else:
            if sys.platform.startswith("linux"):
                self.lily_script = "lilypond"
            else:
                self.lily_script = self.default

    def run(self, wrappers=["", ""]):
        '''
        run the lilypond script on the hierarchy class

        :param wrappers: this is useful for testing: use wrappers to put something around the outputted "lilypond string" from the hierarchy class.
        For example if you're testing a pitch, you might put \relative c {} around the note so that lilypond handles it properly without causing an error

        :return: doesn't return anything, side effect that a PDF should be created.
        '''
        opened_file = open(self.lyfile, 'w')
        lilystring = self.piece_obj.to_lily()
        opened_file.writelines(
            wrappers[0] +
            "\\version \"2.18.2\" \n" +
            lilystring +
            wrappers[1])
        opened_file.close()
        # subprocess.Popen(['sudo', self.lily_script," --output=" +
        #     self.folder, self.lyfile])
        os.system(self.lily_script +
                  " --loglevel=WARNING --output=" +
                  self.folder + " " + self.lyfile
                  )

    def cleanup(self, pdf=False):
        if os.path.exists(self.lyfile):
            os.remove(self.lyfile)

        if pdf:
            if os.path.exists(self.pdf):
                os.remove(self.pdf)
