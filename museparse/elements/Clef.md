Module classes.ObjectHierarchy.ItemClasses.Clef
-----------------------------------------------

Variables
---------
- **clef_type**

    Listing which correlates to each clef's name in lilypond

Classes
-------
#### Clef 
Class which represents clefs. Holds a sign, line and octave_change attrib as these are the various tags
coming in from MusicXML which affect which sign is used.

# Optional inputs

* - sign: the sign to use. Single character generally which when combined with "line" creates the key to pick out from clef_type dict above

* - line: the line on which the clef should rest on

* - octave_change: number of octaves to put the clef up/down by.

##### Ancestors (in MRO)
- classes.ObjectHierarchy.ItemClasses.Clef.Clef

- builtins.object

##### Static methods
- **__init__** (self, **kwargs)

- **toLily** (self)

    Method which converts the object instance and its attributes to a string of lilypond code

    
* :return: str of lilypond code
