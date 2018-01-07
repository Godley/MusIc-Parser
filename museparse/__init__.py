__author__ = 'charlottegodley'
'''This module provides an interface between sheet music input files, python objects and various output formats
Currently, 1 input format is supported - MusicXML - which is parsed via an XML SAX parser. This can be found at
MuseParse.classes.Input.MxmlParser. 1 output format is also supported, which is Lilypond, found at MuseParse.classes.Output.LilypondOutput.
 Lilypond enables the system to output to PDF reliably without having to create a new rendering system. Later, new inputs and outputs may
 be added, but right now these formats give enough functionality for a developer to create a working input and output of sheet music,
 with whatever manipulation of the score they need to do possible when the music is in memory.'''
