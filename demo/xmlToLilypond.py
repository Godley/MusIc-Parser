import sys
import os

from museparse.classes.Output import LilypondOutput
from museparse.classes.Input import MxmlParser

'''
This script can be ran from a console window. It checks for 1 xml file as an argument and then parses/outputs to lilypond
'''


def Run(fname):
    parser = MxmlParser.MxmlParser()
    try:
        pieceObj = parser.parse(fname)
    except BaseException as e:
        return [fname, str(e)]
    render = LilypondOutput.LilypondRenderer(pieceObj, fname)
    try:
        render.run()
    except Exception as e:
        return [render.lyfile, str(e)]
    if not os.path.exists(render.pdf):
        return render.lyfile


if len(sys.argv) > 1:
    file = sys.argv[1]
    print(file)
    Run(file)
