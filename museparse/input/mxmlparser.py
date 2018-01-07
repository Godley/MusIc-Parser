import xml.sax
from xml.sax import make_parser, handler
import copy

from museparse.elements import directions, key, barlinesandmarkers, clef, meter, meta, harmony, note, mark, ornaments, part
from museparse import exceptions
from museparse import helpers
from museparse.tree import piecetree


def IdAsInt(index):
    if index is not None:
        try:
            return int(index)
        except:
            return index


class MxmlParser(object):

    """
    This class encases a standard XML SAX parser in order to parse MusicXML into a tree of objects. Only one is needed for any parse job
    and it can be reused for multiple files.

    ## Optional input

    - excluded - a list of tags which the parser should ignore. functionality of this is not currently implemented.


    """

    data = {}
    '''A dictionary holding data which needs to be tracked by the parser, but is specific to each piece'''

    def clear(self):
        '''
        Method which resets any variables held by this class, so that the parser can be used again
        :return: Nothing
        '''

        self.tags = []
        '''the current list of tags which have been opened in the XML file'''

        self.chars = {}
        '''the chars held by each tag, indexed by their tag name'''

        self.attribs = {}
        '''the attributes of each tag, indexed by their tag name'''

        self.handler = None
        ''' the method which will handle the current tag, and the data currently in the class '''

        self.piece = piecetree.PieceTree()
        '''the class tree top'''

        self.isDynamic = False
        '''Indicator of whether the current thing being processed is a dynamic'''

        self.data["note"] = None
        self.data["direction"] = None
        self.data["expression"] = None
        self.data["degree"] = None
        self.data["frame_note"] = None
        self.data["staff_id"] = 1
        self.data["voice"] = 1
        self.data["handleType"] = ""

    def __init__(self, excluded=[]):
        # stuff for parsing. Tags refers to the xml tag list, chars refers to the content of each tag,
        # attribs refers to attributes of each tag, and handler is a method we
        # call to work with each tag

        self.excluded = excluded
        '''this will be put in later, but parser can take in tags we want to ignore, e.g clefs, BarlinesAndMarkerss etc.'''

        self.structure = {
            "movement-title": SetupPiece,
            "credit": SetupPiece,
            "rights": SetupPiece,
            "creator": SetupPiece,
            "defaults": SetupFormat,
            "part": UpdatePart,
            "score-part": UpdatePart,
            "part-group": UpdatePart,
            "measure": HandleMeasures,
            "note": CreateNote,
            "pitch": HandlePitch,
            "unpitched": HandlePitch,
            "articulations": handleArticulation,
            "fermata": HandleFermata,
            "slur": handleOtherNotations,
            "lyric": handleLyrics,
            "technical": handleOtherNotations,
            "backup": HandleMovementBetweenDurations,
            "forward": HandleMovementBetweenDurations}
        '''Dictionary indicating which tags link to which handler methods'''

        self.multiple_attribs = ["beats", "sign"]
        '''not sure this is needed anymore, but tags which we shouldn't clear the previous data for should be added here'''

        self.closed_tags = ["tie", "chord", "note", "measure", "part",
                            "score-part", "sound", "print", "rest", "slur",
                            "accent", "strong-accent", "staccato",
                            "staccatissimo", "up-bow", "down-bow",
                            "cue", "key", "clef", "part-group", "metronome"]
        '''any tags which close instantly in here'''

        self.end_tag = ["tremolo"]
        self.clear()

    def StartTag(self, name, attrs):
        '''
        A method which is called by the SAX parser when a new tag is encountered
        :param name: name of the tag
        :param attrs: the tag's attributes
        :return: none, side effect of modifying bits of the current class
        '''
        if name not in self.excluded:
            if name in self.structure.keys():
                self.handler = self.structure[name]

            self.tags.append(name)
            if attrs is not None:
                self.attribs[name] = attrs
            self.isDynamic = CheckDynamics(name)
            if self.isDynamic and "dynamics" in self.tags:
                self.handler(
                    self.tags, self.attribs, self.chars, self.piece, self.data)
            if name in self.closed_tags and self.handler is not None:
                self.handler(
                    self.tags, self.attribs, self.chars, self.piece, self.data)

    def validateData(self, text):
        '''
        Method which validates the data from each tag, to check whether it is an empty string
        :param text: data to be validated
        :return: True or False depending on the result
        '''
        if text == "\n":
            return False
        for c in text:
            try:
                if str(c) != " ":
                    return True
            except:
                return False
        return False

    def NewData(self, text):
        '''
        Method which is called by the SAX parser upon encountering text inside a tag
        :param text: the text encountered
        :return: None, has side effects modifying the class itself
        '''
        sint = ignore_exception(ValueError)(int)
        if len(self.tags) > 0:
            if self.tags[-1] == "beat-type" or self.tags[-1] == "beats":
                if sint(text) is int:
                    self.chars[self.tags[-1]] = text

        if self.validateData(text):
            if len(self.tags) > 0:
                if self.tags[-1] not in self.chars:
                    self.chars[self.tags[-1]] = text
                else:
                    self.chars[self.tags[-1]] += text

    def CopyNote(self, part, measure_id, new_note):
        '''
         handles copying the latest note into the measure note list.
         done at end of note loading to make sure staff_id is right as staff id could be encountered
         any point during the note tag
        :param part: the part class to copy it into
        :param measure_id: the id of the measure in which the note belongs
        :param new_note: the new note class to be copied in
        :return: None, side effects modifying the piece tree
        '''

        if part.getMeasure(measure_id, self.data["staff_id"]) is None:
            part.addEmptyMeasure(measure_id, self.data["staff_id"])
        measure = part.getMeasure(measure_id, self.data["staff_id"])
        voice_obj = measure.getVoice(self.data["voice"])
        if voice_obj is None:
            measure.addVoice(id=self.data["voice"])
            voice_obj = measure.getVoice(self.data["voice"])
        add = True
        notes = voice_obj.GetChildrenIndexes()
        for n in notes:
            no = voice_obj.GetChild(n)
            if new_note == no:
                add = False
                break
        if add:
            chord = False
            if hasattr(new_note, "chord"):
                chord = new_note.chord

            measure.addNote(new_note, self.data["voice"], chord=chord)
            if hasattr(
                    new_note, "BarlinesAndMarkersRest") and new_note.BarlinesAndMarkersRest:
                measure.rest = True
                voice_obj.rest = True

    def ResetHandler(self, name):
        '''
        Method which assigns handler to the tag encountered before the current, or else
        sets it to None

        :param name: name of the latest tag

        :return:
        '''
        if name in self.tags:
            if len(self.tags) > 1:
                key = len(self.tags) - 2
                self.handler = None
                while key >= 0:
                    if self.tags[key] in self.structure:
                        self.handler = self.structure[self.tags[key]]
                        break
                    key -= 1

            else:
                self.handler = None

    def EndTag(self, name):
        '''
        Method called by the SAX parser when a tag is ended

        :param name: the name of the tag

        :return: None, side effects
        '''
        if self.handler is not None and not self.isDynamic and name not in self.closed_tags:
            self.handler(
                self.tags, self.attribs, self.chars, self.piece, self.data)

        self.ResetHandler(name)

        if name in self.tags:
            self.tags.remove(name)

        if name == "direction":
            # Copy the direction into the appropriate place, and then clear the
            # direction cache
            if self.data["direction"] is not None:
                measure_id = IdAsInt(
                    helpers.GetID(
                        self.attribs,
                        "measure",
                        "number"))
                part_id = helpers.GetID(self.attribs, "part", "id")
                part = self.piece.getPart(part_id)
                if part is not None:
                    if part.getMeasure(measure_id, self.data[
                                       "staff_id"]) is None:
                        part.addEmptyMeasure(measure_id, self.data["staff_id"])
                    measure = part.getMeasure(
                        measure_id, self.data["staff_id"])
                    measure.addDirection(
                        copy.deepcopy(self.data["direction"]), self.data["voice"])
                self.data["direction"] = None

            if self.data["expression"] is not None:
                # copy the expression into the appropriate place, then clear
                # the expression cache
                measure_id = IdAsInt(
                    helpers.GetID(
                        self.attribs,
                        "measure",
                        "number"))
                part_id = helpers.GetID(self.attribs, "part", "id")
                part = self.piece.getPart(part_id)
                if part is not None:
                    if part.getMeasure(measure_id, self.data[
                                       "staff_id"]) is None:
                        part.addEmptyMeasure(measure_id, self.data["staff_id"])
                    measure = part.getMeasure(
                        measure_id, self.data["staff_id"])
                    measure.addExpression(
                        copy.deepcopy(self.data["expression"]), self.data["voice"])
                self.data["expression"] = None

        if name == "part":
            # do a few checks to confirm barlines are in the right places and
            # to make sure there's no tab in the piece
            part_id = helpers.GetID(self.attribs, "part", "id")
            part = self.piece.getPart(part_id)
            if part is not None:
                part.DoBarlineChecks()
                result = part.CheckIfTabStaff()
                if result is not None:
                    if "TAB" in result:
                        self.piece.removePart(part_id)
                        raise(
                            exceptions.TabNotImplementedException("Tab notation found: stopping"))
                    if "DRUM" in result:
                        self.piece.removePart(part_id)
                        raise(
                            exceptions.DrumNotImplementedException("Drum Tab notation found: stopping"))

        if name == "measure":
            # check for a few issues such as divisions not existing in certain
            # BarlinesAndMarkerss
            part_id = helpers.GetID(self.attribs, "part", "id")
            measure_id = IdAsInt(
                helpers.GetID(
                    self.attribs,
                    "measure",
                    "number"))
            part = self.piece.getPart(part_id)
            if part is None:
                part = self.piece.getLastPart()
            part.CheckMeasureDivisions(measure_id)
            part.CheckMeasureMeter(measure_id)
            part.CheckPreviousBarline(self.data["staff_id"])

            measure = part.getMeasure(measure_id, self.data["staff_id"])
            measure.RunVoiceChecks()
            self.data["staff_id"] = 1
            self.data["voice"] = 1

        # remove the latest data from the other caches
        if name in self.attribs:
            self.attribs.pop(name)
        if name in self.chars:
            self.chars.pop(name)

        if name == "note":
            # copy accross the new note and then clear the cache
            measure_id = IdAsInt(
                helpers.GetID(
                    self.attribs,
                    "measure",
                    "number"))
            part_id = helpers.GetID(self.attribs, "part", "id")
            part = self.piece.getPart(part_id)
            if part is None:
                part = self.piece.getLastPart()
            if part is not None:
                self.CopyNote(
                    part, measure_id, copy.deepcopy(self.data["note"]))
            self.data["note"] = None

        if name == "degree":
            self.data["degree"] = None
        if name == "frame-note":
            self.data["frame_note"] = None

    def parse(self, file):
        '''
        Method the programmer should call when ready to parse a file.
        :param file: exact file path of the file to be processed
        :return: PieceTree object representing the file in memory
        '''
        parser = make_parser()
        self.clear()

        class Extractor(xml.sax.ContentHandler):

            def __init__(self, parent):
                self.parent = parent

            def startElement(self, name, attrs):
                attribs = {}
                for attrname in attrs.getNames():
                    attrvalue = attrs.get(attrname)
                    attribs[attrname] = attrvalue
                self.parent.StartTag(name, attribs)

            def characters(self, text):
                self.parent.NewData(text)

            def endElement(self, name):
                self.parent.EndTag(name)
        parser.setContentHandler(Extractor(self))
        # OFFLINE MODE
        parser.setFeature(handler.feature_external_ges, False)
        fob = open(file, 'r')
        parser.parse(fob)
        return self.piece


def YesNoToBool(entry):
    '''
    Method which takes in either yes or no and converts it to bool. Often found in MusicXML.
    :param entry: the word to convert
    :return: True/False
    '''
    if entry == "yes":
        return True
    if entry == "no":
        return False


def ignore_exception(IgnoreException=Exception, DefaultVal=None):
    """ Decorator for ignoring exception from a function
    e.g.   @ignore_exception(DivideByZero)
    e.g.2. ignore_exception(DivideByZero)(Divide)(2/0)
    borrowed from: http://stackoverflow.com/questions/2262333/is-there-a-built-in-or-more-pythonic-way-to-try-to-parse-a-string-to-an-integer
    """

    def dec(function):
        def _dec(*args, **kwargs):
            try:
                return function(*args, **kwargs)
            except IgnoreException:
                return DefaultVal

        return _dec

    return dec


# HANDLER METHODS: see tag correlations inside the MusicXML parser class
# init method.
def SetupPiece(tag, attrib, content, piece, data):
    return_val = None
    if content is not [] and len(tag) > 0:
        title = None
        composer = None
        if tag[-1] == "movement-title":
            return_val = 1
            if "movement-title" in content:
                title = content["movement-title"]
        if tag[-1] == "creator":
            return_val = 1
            if "creator" in attrib:
                if "type" in attrib["creator"]:
                    if attrib["creator"]["type"] == "composer":
                        if "creator" in content:
                            composer = content["creator"]
        if tag[-1] == "movement-title" or "creator":
            if not hasattr(piece.GetItem(), "meta"):
                piece.GetItem().meta = meta.meta(
                    composer=composer,
                    title=title)

            else:
                if composer is not None:
                    piece.GetItem().meta.composer = composer
                if title is not None:
                    piece.GetItem().meta.title = title
        if tag[-1] == "rights":
            if "rights" in content:
                rights = content["rights"] + " "
                if hasattr(piece.GetItem(), "meta"):
                    if not hasattr(piece.GetItem().meta, "copyright"):
                        piece.GetItem().meta.copyright = ""
                    piece.GetItem().meta.copyright += rights
                else:
                    piece.GetItem().meta = meta.meta(copyright=rights)
        if "credit" in tag:
            page = 0
            if "credit" in attrib:
                if "page" in attrib["credit"]:
                    page = int(attrib["credit"]["page"])
            if tag[-1] == "credit-type":
                data["handleType"] = content["credit-type"]
            if tag[-1] == "credit-words":
                x = None
                y = None
                size = None
                justify = None
                valign = None
                text = None
                if "credit-words" in attrib:
                    temp = attrib["credit-words"]

                    if "default-x" in temp:
                        x = float(temp["default-x"])
                    if "default-y" in temp:
                        y = float(temp["default-y"])
                    if "font-size" in temp:
                        size = float(temp["font-size"])
                    if "justify" in temp:
                        justify = temp["justify"]
                        if justify == "center" and data["handleType"] == "":
                            data["handleType"] = "title"
                        if justify == "right" and data["handleType"] == "":
                            data["handleType"] = "composer"
                    if "valign" in temp:
                        valign = temp["valign"]
                        if valign == "bottom" and data["handleType"] == "":
                            data["handleType"] = "rights"

                if "credit-words" in content:
                    text = content["credit-words"]

                if data["handleType"] == "":
                    credit = directions.CreditText(
                        page=page,
                        x=x,
                        y=y,
                        size=size,
                        justify=justify,
                        valign=valign,
                        text=text)
                    if not hasattr(piece.GetItem(), "meta"):
                        piece.GetItem().meta = meta.meta()
                    piece.GetItem().meta.add_credit(credit)
                else:
                    if data["handleType"] == "composer":
                        if not hasattr(piece.GetItem().meta, "composer"):
                            piece.GetItem().meta.composer = text
                        else:
                            if text.replace(
                                " ",
                                "") not in piece.GetItem().meta.composer.replace(
                                " ",
                                "") and piece.GetItem().meta.composer.replace(
                                " ",
                                "") not in text.replace(
                                " ",
                                    ""):
                                piece.GetItem().meta.composer += text
                    if data["handleType"] == "rights":
                        if not hasattr(piece.GetItem().meta, "copyright"):
                            piece.GetItem().meta.copyright = text
                        else:
                            if text.replace(
                                " ",
                                "") not in piece.GetItem().meta.copyright.replace(
                                " ",
                                "") and piece.GetItem().meta.copyright.replace(
                                " ",
                                "") not in text.replace(
                                " ",
                                    ""):
                                piece.GetItem().meta.copyright += text
                    if data["handleType"] == "title":
                        if not hasattr(piece.GetItem().meta, "title"):
                            piece.GetItem().meta.title = text
                        else:
                            if text.replace(
                                " ",
                                "") not in piece.GetItem().meta.title.replace(
                                " ",
                                "") and piece.GetItem().meta.title.replace(
                                " ",
                                "") not in text.replace(
                                " ",
                                    ""):
                                piece.GetItem().meta.title += text
                    if data["handleType"] == "page number":
                        if not hasattr(piece.GetItem().meta, "pageNum"):
                            piece.GetItem().meta.pageNum = True
                    data["handleType"] = ""
    return return_val


def UpdatePart(tag, attrib, content, piece, data):
    part_id = helpers.GetID(attrib, "part", "id")
    if part_id is None:
        part_id = helpers.GetID(attrib, "score-part", "id")
    return_val = None
    if len(tag) > 0:
        if "part-group" in tag:
            index = 0
            type = ""
            if "part-group" in attrib:
                if "number" in attrib["part-group"]:
                    index = int(attrib["part-group"]["number"])
                if "type" in attrib["part-group"]:
                    type = attrib["part-group"]["type"]
            if type != "":
                if type == "start":
                    piece.startGroup(index)
                if type == "stop":
                    piece.stopGroup(index)
        if "score-part" in tag:
            if part_id is None:
                raise(
                    exceptions.NoScorePartException("ERROR IN UPDATEPART: no score-part id found"))
            elif piece.getPart(part_id) is None:
                piece.addPart(part.Part(), index=part_id)
                return_val = 1
            if "part-name" in tag:
                if "part-name" in content and part_id is not None:
                    name_rplc = content["part-name"].replace("\r", "\n")
                    piece.getPart(part_id).GetItem().name = name_rplc
                    return_val = 1
            if "part-abbreviation" in tag:
                if "part-abbreviation" in content and part_id is not None:
                    piece.getPart(part_id).GetItem().shortname = content[
                        "part-abbreviation"]
    return return_val


def handleArticulation(tag, attrs, content, piece, data):
    if len(tag) > 0:
        if "articulations" in tag:
            if data["note"] is not None:
                accent = None
                if tag[-1] == "accent":
                    accent = mark.Accent()
                if tag[-1] == "strong-accent":
                    s_type = ""
                    if "strong-accent" in attrs:
                        if "type" in attrs["strong-accent"]:
                            s_type = attrs["strong-accent"]["type"]
                    accent = mark.StrongAccent(type=s_type)
                if tag[-1] == "staccato":
                    accent = mark.Staccato()
                if tag[-1] == "staccatissimo":
                    accent = mark.Staccatissimo()
                if tag[-1] == "detached-legato":
                    accent = mark.DetachedLegato()
                if tag[-1] == "tenuto":
                    accent = mark.Tenuto()
                if tag[-1] == "breath-mark":
                    accent = mark.BreathMark()
                if tag[-1] == "caesura":
                    accent = mark.Caesura()
                if accent is not None:
                    if data["note"].search(type(accent)) is None:
                        data["note"].add_notation(accent)
                    accent = None
            return 1
    return None


def HandleMovementBetweenDurations(tags, attrs, chars, piece, data):
    global last_note
    measure_id = IdAsInt(helpers.GetID(attrs, "measure", "number"))

    part_id = helpers.GetID(attrs, "part", "id")
    if part_id is not None:
        if measure_id is not None:
            part = piece.getPart(part_id)
            if part.getMeasure(measure_id, data["staff_id"]) is None:
                part.addEmptyMeasure(measure_id, data["staff_id"])
            measure = part.getMeasure(measure_id, data["staff_id"])
            if "backup" in tags and tags[-1] == "duration":
                part.check_divisions()
                part.Backup(measure_id, duration=float(chars["duration"]))
            if "forward" in tags and tags[-1] == "duration":
                part.check_divisions()
                part.Forward(measure_id, duration=float(chars["duration"]))


def HandleFermata(tags, attrs, chars, piece, data):
    if "fermata" in tags:
        type = None
        symbol = None
        if "fermata" in attrs:
            if "type" in attrs["fermata"]:
                type = attrs["fermata"]["type"]
        if "fermata" in chars:
            symbol = chars["fermata"]
        fermata = mark.Fermata(type=type, symbol=symbol)
        data["note"].add_notation(fermata)
    return None


def handleOtherNotations(tag, attrs, content, piece, data):
    if len(tag) > 0:
        if "notations" in tag:
            if tag[-1] == "slur":

                notation = directions.Slur()
                if "slur" in attrs and "placement" in attrs["slur"]:
                    notation.placement = attrs["slur"]["placement"]

                if "slur" in attrs and "type" in attrs["slur"]:
                    notation.type = attrs["slur"]["type"]
                data["note"].add_slur(notation)
            if tag[-
                   2] == "technical" and tag[-
                                             1] != "bend" and tag[-
                                                                  1] != "hammer-on" and tag[-
                                                                                            1] != "pull-off":
                text = None
                if tag[-1] in content:
                    text = content[tag[-1]]
                data["note"].add_notation(
                    mark.Technique(type=tag[-1], symbol=text))
            elif len(tag) >= 3 and tag[-3] == "technical" and tag[-2] == "bend":
                bend_val = 0
                if tag[-1] in content:
                    bend_val = content[tag[-1]]
                data["note"].add_notation(mark.Bend(value=float(bend_val)))

            return 1
    return None


def HandleMeasures(tag, attrib, content, piece, data):
    part_id = helpers.GetID(attrib, "part", "id")
    measure_id = IdAsInt(helpers.GetID(attrib, "measure", "number"))
    part = None
    key = None
    return_val = None
    if len(tag) > 0 and "measure" in tag:

        if "staff" in tag:
            data["staff_id"] = int(content["staff"])
        if part_id is None:
            part_id = piece.root.GetChildrenIndexes()[-1]
        if part_id is not None:
            part = piece.getPart(part_id)
            if part is None:
                part_id = piece.root.GetChildrenIndexes()[-1]
                part = piece.getPart(part_id)
        measure = None

        if part is not None:
            if tag[-1] == "staves":
                staves = int(content["staves"])
                for staff in range(1, staves + 1):
                    if part.getMeasure(measure_id, staff) is None:
                        part.addEmptyMeasure(measure_id, staff)
            measure = part.getMeasure(
                measure=measure_id, staff=data["staff_id"])
            if measure is None:
                part.addEmptyMeasure(measure_id, data["staff_id"])
                measure = part.getMeasure(measure_id, data["staff_id"])
            if measure is not None:
                key = measure.GetLastKey(voice=data["voice"])
                if key is not None and type(key) is not key.key:
                    key = key.GetItem()
        implicit = helpers.GetID(attrib, "measure", "implicit")
        if implicit is not None:
            measure.partial = YesNoToBool(implicit)
        if tag[-1] == "divisions" and measure is not None:
            measure.divisions = int(content["divisions"])
        if tag[-1] == "key":
            if "key" in attrib:
                if "number" in attrib["key"]:
                    data["staff_id"] = int(attrib["key"]["number"])
                    measure = part.getMeasure(
                        measure=measure_id,
                        staff=data["staff_id"])
                    if measure is None:
                        part.addEmptyMeasure(measure_id, data["staff_id"])
                        measure = part.getMeasure(measure_id, data["staff_id"])
                    if measure is not None:
                        key = measure.GetLastKey(voice=data["voice"])
                        if key is not None and type(key) is not key.key:
                            key = key.GetItem()
                        measure.addKey(key.key(), data["voice"])
                else:
                    part.addKey(key.key(), measure_id)
            else:
                part.addKey(key.key(), measure_id)
        if tag[-1] == "mode" and "key" in tag and measure is not None:
            key = measure.GetLastKey(voice=data["voice"])
            if key is not None and type(key) is not key.key:
                key = key.GetItem()
            if key is not None:
                key.mode = content["mode"]
            return_val = 1
        if tag[-1] == "fifths" and "key" in tag:
            key = measure.GetLastKey(voice=data["voice"])
            if key is not None and type(key) is not key.key:
                key = key.GetItem()
            if key is not None:
                key.fifths = int(content["fifths"])
            return_val = 1

        if tag[-1] == "beats" and ("time" in tag or "meter" in tag):
            symbol = helpers.GetID(attrib, "time", "symbol")
            if hasattr(measure, "meter"):
                measure.meter.beats = int(content["beats"])
                if symbol is not None:
                    measure.meter.style = symbol
            else:
                measure.meter = meter.meter(
                    beats=int(
                        content["beats"]),
                    style=symbol)
            return_val = 1
        if tag[-1] == "beat-type" and ("time" in tag or "meter" in tag):
            symbol = helpers.GetID(attrib, "time", "symbol")
            if hasattr(measure, "meter"):
                measure.meter.type = int(content["beat-type"])
                if symbol is not None:
                    measure.meter.style = symbol
            else:
                measure.meter = meter.meter(
                    type=int(
                        content["beat-type"]),
                    style=symbol)
            return_val = 1
        if "clef" in tag:
            handleClef(tag, attrib, content, piece, data)
        if "transpose" in tag:
            if "diatonic" in tag:
                if hasattr(measure, "transpose"):
                    measure.transpose.diatonic = content["diatonic"]
                else:
                    measure.transpose = barlinesandmarkers.Transposition(
                        diatonic=content["diatonic"])
            if "chromatic" in tag:
                if hasattr(measure, "transpose"):
                    measure.transpose.chromatic = content["chromatic"]
                else:
                    measure.transpose = barlinesandmarkers.Transposition(
                        chromatic=content["chromatic"])
            if "octave-change" in tag:
                if hasattr(measure, "transpose"):
                    measure.transpose.octave = content["octave-change"]
                else:
                    measure.transpose = barlinesandmarkers.Transposition(
                        octave=content["octave-change"])
            return_val = 1
        if "print" in tag:
            part = piece.getPart(part_id)
            staves = piece.getPart(part_id).GetChildrenIndexes()
            if "print" in attrib:
                if "new-system" in attrib["print"]:
                    for staff in staves:
                        if part.getMeasure(measure_id, staff) is None:
                            part.addEmptyMeasure(measure_id, staff)
                        measure = part.getMeasure(measure_id, staff)
                        measure.newSystem = YesNoToBool(
                            attrib["print"]["new-system"])
                if "new-page" in attrib["print"]:
                    for staff in staves:
                        if part.getMeasure(measure_id, staff) is None:
                            part.addEmptyMeasure(measure_id, staff)
                        measure = part.getMeasure(measure_id, staff)
                        measure.newPage = YesNoToBool(
                            attrib["print"]["new-page"])
            return_val = 1

        if "harmony" in tag:
            root = None
            kind = None
            bass = None
            if data["direction"] is None:
                data["direction"] = harmony.Harmony(kind=kind)
            else:
                data["direction"].kind = kind

            if "root" in tag:
                if not hasattr(data["direction"], "root"):
                    root = harmony.harmonyPitch()
                    data["direction"].root = root
                else:
                    root = data["direction"].root
                if tag[-1] == "root-step":
                    if "root-step" in content:
                        root.step = content["root-step"]
                if tag[-1] == "root-alter":
                    if "root-alter" in content:
                        root.alter = content["root-alter"]

            if "kind" in tag:
                if not hasattr(data["direction"], "kind") or data[
                        "direction"].kind is None:
                    kind = harmony.Kind()
                    data["direction"].kind = kind
                elif data["direction"].kind is not None:
                    kind = data["direction"].kind
                if "kind" in content:
                    kind.value = content["kind"]
                if "kind" in attrib:
                    if "text" in attrib["kind"]:
                        kind.text = attrib["kind"]["text"]
                    if "halign" in attrib["kind"]:
                        kind.halign = attrib["kind"]["halign"]
                    if "parenthesis-degrees" in attrib["kind"]:
                        kind.parenthesis = attrib[
                            "kind"]["parenthesis-degrees"]

            if tag[-1] == "voice":
                data["voice"] = int(content["voice"])

            if "bass" in tag:
                if not hasattr(data["direction"], "bass"):
                    data["direction"].bass = harmony.harmonyPitch()
                if "bass-step" in tag and "bass-step" in content:
                    data["direction"].bass.step = content["bass-step"]
                if "bass-alter" in tag and "bass-alter" in content:
                    data["direction"].bass.alter = content["bass-alter"]
            frame = None

            if "degree" in tag:
                if data["degree"] is None:
                    data["degree"] = harmony.Degree()
                    data["direction"].degrees.append(data["degree"])

                if "degree-value" in tag:
                    if "degree-value" in content:
                        data["degree"].value = content["degree-value"]
                if "degree-alter" in tag:
                    if "degree-alter" in content:
                        data["degree"].alter = content["degree-alter"]
                if "degree-type" in tag:
                    if "degree-type" in content:
                        data["degree"].type = content["degree-type"]
                    if "degree-type" in attrib:
                        if "text" in attrib["degree-type"]:
                            data["degree"].display = attrib[
                                "degree-type"]["text"]

            if "frame" in tag:
                if not hasattr(data["direction"], "frame"):
                    data["direction"].frame = harmony.Frame()
                if "first-fret" in tag:
                    data["direction"].frame.firstFret = True
                    if "first-fret" in content:
                        if "first-fret" not in attrib:
                            data["direction"].frame.firstFret = [
                                content["first-fret"]]
                        else:
                            data["direction"].frame.firstFret = [
                                content["first-fret"]]
                            if "text" in attrib["first-fret"]:
                                data["direction"].frame.firstFret.append(
                                    attrib["first-fret"]["text"])
                if "frame-strings" in tag and "frame-strings" in content:
                    data["direction"].frame.strings = content["frame-strings"]
                if "frame-frets" in tag and "frame-frets" in content:
                    data["direction"].frame.frets = content["frame-frets"]
                if "frame-note" in tag:
                    if data["frame_note"] is None:
                        data["frame_note"] = harmony.FrameNote()

                    if "string" in tag and "string" in content:
                        data["frame_note"].string = content["string"]
                        data["direction"].frame.notes[
                            int(content["string"])] = data["frame_note"]
                    if "fret" in tag and "fret" in content:
                        data["frame_note"].fret = content["fret"]
                    if "barre" in tag and "barre" in attrib:
                        data["frame_note"].barre = attrib["barre"]["type"]
                    if "fingering" in tag and "fingering" in content:
                        data["frame_note"].fingering = content["fingering"]
    handleBarline(tag, attrib, content, piece, data)
    HandleDirections(tag, attrib, content, piece, data)
    handleArticulation(tag, attrib, content, piece, data)

    return return_val


def handleClef(tag, attrib, content, piece, data):
    data["staff_id"] = IdAsInt(helpers.GetID(attrib, "clef", "number"))
    if data["staff_id"] is None:
        data["staff_id"] = 1
    measure_id = IdAsInt(helpers.GetID(attrib, "measure", "number"))
    part_id = helpers.GetID(attrib, "part", "id")
    part = piece.getPart(part_id)
    if part is not None:
        BarlinesAndMarkersNode = part.getMeasure(measure_id, data["staff_id"])
        if BarlinesAndMarkersNode is None:
            part.addEmptyMeasure(measure_id, data["staff_id"])
            BarlinesAndMarkersNode = part.getMeasure(
                measure_id, data["staff_id"])
        if tag[-1] == "clef":
            part.addClef(
                clef.Clef(), measure_id, data["staff_id"], data["voice"])
        if BarlinesAndMarkersNode is not None:
            clef = BarlinesAndMarkersNode.GetLastClef(voice=data["voice"])
            if clef is not None and type(clef) is not clef.Clef:
                clef = clef.GetItem()
            sign = None
            line = None
            octave = None
            if tag[-1] == "sign":
                sign = content["sign"]
                if sign == "percussion":
                    part.drum = True
                else:
                    part.drum = False
                if sign == "tab":
                    part.tab = True
                else:
                    part.tab = False
            if tag[-1] == "line":
                line = int(content["line"])
            if tag[-1] == "clef-octave-change":
                octave = int(content["clef-octave-change"])
            if clef is not None:
                if sign is not None:
                    clef.sign = sign
                if line is not None:
                    clef.line = int(line)
                if octave is not None:
                    clef.octave_change = octave
    data["staff_id"] = 1


def handleBarline(tag, attrib, content, piece, data):
    part_id = helpers.GetID(attrib, "part", "id")
    measure_id = IdAsInt(helpers.GetID(attrib, "measure", "number"))
    measure = None
    times = 2
    if part_id is not None and measure_id is not None:
        part = piece.getPart(part_id)
        if part is None:
            part = piece.getLastPart()

        if part.getMeasure(measure_id, int(data["staff_id"])) is None:
            part.addEmptyMeasure(measure_id, int(data["staff_id"]))
        measure = part.getMeasure(measure_id, int(data["staff_id"]))
    if "barline" in tag and measure is not None:
        location = helpers.GetID(attrib, "barline", "location")
        barline = None
        style = None
        repeat = None
        ending = None
        if tag[-1] == "ending":
            btype = None
            number = None
            if "ending" in attrib:
                if "number" in attrib["ending"]:
                    if measure.GetBarline(location) is None or not hasattr(
                            measure.GetBarline(location),
                            "ending"):
                        num_str = attrib["ending"]["number"]
                        split = num_str.split(",")
                        number = int(split[-1])
                    else:
                        measure.GetBarline(location).ending.number = int(
                            attrib["ending"]["number"])
                if "type" in attrib["ending"]:
                    if location not in measure.barlines or not hasattr(
                            measure.GetBarline(location),
                            "ending"):
                        btype = attrib["ending"]["type"]
                    else:
                        measure.GetBarline(
                            location).ending.type = attrib["ending"]["type"]

            ending = barlinesandmarkers.EndingMark(type=btype, number=number)

            if location in measure.barlines:
                measure.GetBarline(location).ending = ending

        if tag[-1] == "bar-style":
            if location not in measure.barlines:
                style = content["bar-style"]
            else:
                measure.GetBarline(location).style = style
        if tag[-1] == "repeat":
            if "repeat" in attrib:
                times = helpers.GetID(attrib, "repeat", "times")
                if times is not None:
                    times = int(times)
                if "direction" in attrib["repeat"]:
                    barline = measure.GetBarline(location)

                    repeat = attrib["repeat"]["direction"]
                    if hasattr(barline, "ending"):
                        position = -2
                        index = part.getMeasureIDAtPosition(
                            position,
                            staff=data["staff_id"])
                        if index is not None:
                            right_barline = part.getMeasure(
                                index,
                                data["staff_id"]).GetBarline("right")
                            if right_barline is not None and hasattr(
                                    right_barline,
                                    "ending"):
                                position -= 1
                                index = part.getMeasureIDAtPosition(
                                    position,
                                    staff=data["staff_id"])
                            part.AddBarline(
                                measure=index,
                                staff=data["staff_id"],
                                item=barlinesandmarkers.Barline(
                                    repeat="backward",
                                    repeatNum=times),
                                location="right")
                            #part.AddBarline(measure=index, staff=staff_id, item=barlinesandmarkers.Barline(repeat="forward"), location="left")
                            if barline.ending.number == 1:
                                barline.repeat = "backward-barline"

                    else:
                        if barline is not None:
                            barline.repeat = repeat
                            if times is not None:
                                barline.repeatNum = times
                            part.AddBarline(
                                item=barline,
                                measure=measure_id,
                                staff=data["staff_id"],
                                location=location)

        if location not in measure.barlines:
            if barline is None:
                barline = barlinesandmarkers.Barline(
                    style=style,
                    repeat=repeat,
                    ending=ending)
            part.AddBarline(
                measure=measure_id,
                staff=data["staff_id"],
                item=barline,
                location=location)


def CheckID(tag, attrs, string, id_name):
    if string in tag:
        return attrs[string][id_name]


def CreateNote(tag, attrs, content, piece, data):
    ret_value = None

    if len(tag) > 0 and "note" in tag:

        if tag[-1] == "staff":
            data["staff_id"] = int(content["staff"])
        if "note" in tag and data["note"] is None:
            data["note"] = note.Note()
            ret_value = 1
        if "note" in attrs:
            if "print-object" in attrs["note"]:
                result = YesNoToBool(attrs["note"]["print-object"])
                data["note"].print = result
        if "rest" in tag:
            rest_measure = helpers.GetID(attrs, "rest", "measure")
            if rest_measure is not None:
                value = YesNoToBool(rest_measure)
                data["note"].measureRest = value
            data["note"].rest = True
        if "cue" in tag:
            data["note"].cue = True

        if tag[-1] == "grace":
            slash = False
            if "grace" in attrs:
                if "slash" in attrs["grace"]:
                    slash = YesNoToBool(attrs["grace"]["slash"])
            data["note"].add_notation(note.GraceNote(slash=slash, first=True))
        if tag[-1] == "duration" and "note" in tag:
            if not hasattr(data["note"], "duration"):
                data["note"].duration = float(content["duration"])

        if tag[-1] == "type":
            data["note"].set_type(content["type"])

        if tag[-1] == "dot":
            data["note"].add_dot()
        if tag[-1] == "tie":
            data["note"].add_tie(attrs["tie"]["type"])
        if "chord" in tag:
            data["note"].chord = True
        if tag[-1] == "stem":
            data["note"].stem = note.Stem(content["stem"])
        if tag[-1] == "voice":
            data["voice"] = int(content["voice"])

        if tag[-1] == "beam":
            type = ""
            if "beam" in content:
                type = content["beam"]
            if "beam" in attrs:
                id = int(attrs["beam"]["number"])
            else:
                id = len(data["note"].beams)
            part_id = helpers.GetID(attrs, "part", "id")
            part = piece.getPart(part_id)
            part.NewBeam(type, data["staff_id"])
            data["note"].add_beam(id, note.Beam(type))

        if tag[-1] == "accidental":
            if not hasattr(data["note"], "pitch"):
                data["note"].pitch = note.Pitch()
                if "accidental" in content:
                    data["note"].pitch.accidental = content["accidental"]

            else:
                if "accidental" in content:
                    data["note"].pitch.accidental = content["accidental"]
        if tag[-1] == "staff":
            data["staff_id"] = int(content["staff"])
    HandleNoteheads(tag, attrs, content, piece, data)
    HandleArpeggiates(tag, attrs, content, piece, data)
    HandleSlidesAndGliss(tag, attrs, content, piece, data)
    handleLyrics(tag, attrs, content, piece, data)
    handleOrnaments(tag, attrs, content, piece, data)
    handleOtherNotations(tag, attrs, content, piece, data)
    handleTimeMod(tag, attrs, content, piece, data)
    return ret_value


def HandleNoteheads(tags, attrs, content, piece, data):
    if "note" in tags:
        if tags[-1] == "notehead":
            data["note"].notehead = note.Notehead()
            if "notehead" in attrs:
                if "filled" in attrs["notehead"]:
                    filled = YesNoToBool(attrs["notehead"]["filled"])
                    data["note"].notehead.filled = filled
            if "notehead" in content:
                data["note"].notehead.type = content["notehead"]


def HandleArpeggiates(tags, attrs, content, piece, data):
    if len(tags) > 0:
        if tags[-1] == "arpeggiate":
            data["direction"] = None
            if "arpeggiate" in attrs:
                if "direction" in attrs["arpeggiate"]:
                    data["direction"] = attrs["arpeggiate"]["direction"]
            arpegg = note.Arpeggiate(direction=data["direction"])
            data["note"].add_notation(arpegg)
        if tags[-1] == "non-arpeggiate":
            type = None
            if "non-arpeggiate" in attrs:
                if "type" in attrs["non-arpeggiate"]:
                    type = attrs["non-arpeggiate"]["type"]
            narpegg = note.NonArpeggiate(type=type)
            data["note"].add_notation(narpegg)


def HandleSlidesAndGliss(tags, attrs, content, piece, data):
    type = None
    number = None
    lineType = None
    if "slide" in tags or "glissando" in tags:
        if tags[-1] in attrs:
            if "type" in attrs[tags[-1]]:
                type = attrs[tags[-1]]["type"]
            if "line-type" in attrs[tags[-1]]:
                lineType = attrs[tags[-1]]["line-type"]
            if "number" in attrs[tags[-1]]:
                number = int(attrs[tags[-1]]["number"])
    if "slide" in tags:
        slide = note.Slide(type=type, lineType=lineType, number=number)
        data["note"].add_notation(slide)
    if "glissando" in tags:
        gliss = note.Glissando(type=type, lineType=lineType, number=number)
        data["note"].add_notation(gliss)


def handleOrnaments(tags, attrs, content, piece, data):
    if "ornaments" in tags:
        if tags[-1] == "inverted-mordent":
            data["note"].add_notation(ornaments.InvertedMordent())
        if tags[-1] == "mordent":
            data["note"].add_notation(ornaments.Mordent())
        if tags[-1] == "trill-mark":
            data["note"].add_notation(ornaments.Trill())
        if tags[-1] == "wavy-line":
            type = ""
            if "wavy-line" in attrs:
                if "type" in attrs["wavy-line"]:
                    type = attrs["wavy-line"]["type"]
                else:
                    type = True
            data["note"].add_notation(ornaments.TrillSpanner(line=type))
        if tags[-1] == "turn":
            data["note"].add_notation(ornaments.Turn())
        if tags[-1] == "inverted-turn":
            data["note"].add_notation(ornaments.InvertedTurn())
        if tags[-1] == "tremolo":
            type = None
            value = None
            if "tremolo" in attrs:
                if "type" in attrs["tremolo"]:
                    type = attrs["tremolo"]["type"]
            if "tremolo" in content:
                value = int(content["tremolo"])
            data["note"].add_notation(
                ornaments.Tremolo(type=type, value=value))


def SetupFormat(tags, attrs, text, piece, data):
    return None


def HandlePitch(tags, attrs, text, piece, data):
    return_val = None
    if len(tags) > 0:
        if "pitch" or "unpitched" in tags:
            if not hasattr(data["note"], "pitch") and data["note"] is not None:
                data["note"].pitch = note.Pitch()
            if "unpitched" in tags:
                data["note"].pitch.unpitched = True
            if "step" in tags[-1]:
                if "step" not in text:
                    data["note"].pitch.step = text["display-step"]
                else:
                    data["note"].pitch.step = text["step"]
                return_val = 1
            if tags[-1] == "alter":
                data["note"].pitch.alter = int(text["alter"])
                return_val = 1
            if "octave" in tags[-1]:
                if "octave" not in text:
                    data["note"].pitch.octave = text["display-octave"]
                else:
                    data["note"].pitch.octave = text["octave"]
                return_val = 1
    return return_val


def HandleDirections(tags, attrs, chars, piece, data):
    global expressions, items
    return_val = None
    if len(tags) == 0:
        return None

    if "direction" in tags:
        measure_id = IdAsInt(helpers.GetID(attrs, "measure", "number"))
        part_id = helpers.GetID(attrs, "part", "id")
        measure = None
        if measure_id is not None and part_id is not None:
            measure = piece.getPart(part_id).getMeasure(
                measure_id, data["staff_id"])
            if measure is None:
                piece.getPart(part_id).addEmptyMeasure(
                    measure_id, data["staff_id"])
                measure = piece.getPart(part_id).getMeasure(
                    measure_id,
                    data["staff_id"])
        placement = None
        if measure is None:
            return None
        if tags[-1] == "staff":
            data["staff_id"] = int(chars["staff"])
        if "direction" in attrs:
            if "placement" in attrs["direction"]:
                placement = attrs["direction"]["placement"]

        if tags[-1] == "words":
            return_val = 1

            size = None
            font = None
            text = None
            if "words" in chars:
                text = chars["words"]

            if "words" in attrs:
                if "font-size" in attrs["words"]:
                    size = attrs["words"]["font-size"]
                if "font-family" in attrs["words"]:
                    font = attrs["words"]["font-family"]
            data["direction"] = directions.Direction(
                font=font,
                text=text,
                size=size,
                placement=placement)
        if tags[-1] == "voice":
            data["voice"] = int(chars["voice"])
        if tags[-1] == "rehearsal":
            return_val = 1

            size = None
            font = None
            text = chars["rehearsal"]

            if "words" in attrs:
                if "font-size" in attrs["words"]:
                    size = attrs["words"]["font-size"]
                if "font-family" in attrs["words"]:
                    font = attrs["words"]["font-family"]
            data["direction"] = directions.RehearsalMark(
                font=font,
                text=text,
                size=size,
                placement=placement)
        if tags[-1] == "metronome":
            if data["direction"] is not None:
                if type(data["direction"]) != directions.Metronome:
                    new_obj = directions.Metronome(
                        text=copy.deepcopy(data["direction"]))
                    data["direction"] = new_obj
        if "metronome" in tags:
            if tags[-1] == "beat-unit":
                return_val = 1
                unit = chars["beat-unit"]
                if data["direction"] is None:
                    data["direction"] = directions.Metronome(
                        placement=placement,
                        beat=unit)
                else:
                    if not hasattr(
                            data["direction"],
                            "beat") or data["direction"].beat is None:
                        data["direction"].beat = unit
                    else:
                        data["direction"].secondBeat = unit
                    data["direction"].placement = placement
                if "metronome" in attrs:
                    if "font-family" in attrs["metronome"]:
                        data["direction"].font = attrs[
                            "metronome"]["font-family"]
                    if "font-size" in attrs["metronome"]:
                        data["direction"].size = attrs[
                            "metronome"]["font-size"]
                    if "parentheses" in attrs["metronome"]:
                        data["direction"].parentheses = YesNoToBool(
                            attrs["metronome"]["parentheses"])
            if tags[-1] == "per-minute":
                return_val = 1
                pm = chars["per-minute"]

                if data["direction"] is None:
                    data["direction"] = directions.Metronome(min=pm)
                else:
                    data["direction"].min = pm
                if "metronome" in attrs:
                    if "font-family" in attrs["metronome"]:
                        data["direction"].font = attrs[
                            "metronome"]["font-family"]
                    if "font-size" in attrs["metronome"]:
                        data["direction"].size = float(
                            attrs["metronome"]["font-size"])
                    if "parentheses" in attrs["metronome"]:
                        data["direction"].parentheses = YesNoToBool(
                            attrs["metronome"]["parentheses"])
        if tags[-1] == "wedge":
            w_type = None
            if "wedge" in attrs:
                if "type" in attrs["wedge"]:
                    w_type = attrs["wedge"]["type"]
            data["expression"] = directions.Wedge(
                placement=placement, type=w_type)

        if len(tags) > 1:
            if tags[-2] == "dynamics" and tags[-1] != "other-dynamics":
                data["expression"] = directions.Dynamic(
                    placement=placement, mark=tags[-1])
            if tags[-2] == "dynamics" and tags[-1] == "other-dynamics":
                data["expression"] = directions.Dynamic(
                    placement=placement,
                    text=chars["other-dynamics"])

        if "sound" in tags:
            return_val = 1
            if "sound" in attrs:
                if "dynamics" in attrs["sound"]:
                    measure.volume = attrs["sound"]["dynamics"]
                if "tempo" in attrs["sound"]:
                    measure.tempo = attrs["sound"]["tempo"]
        l_type = None
        if tags[-1] in ["wavy-line", "octave-shift", "pedal", "bracket"]:
            if tags[-1] in attrs:
                if "type" in attrs[tags[-1]]:
                    l_type = attrs[tags[-1]]["type"]
        if "octave-shift" in tags:
            amount = None
            font = None
            if "octave-shift" in attrs:
                if "size" in attrs["octave-shift"]:
                    amount = int(attrs["octave-shift"]["size"])
                if "font" in attrs["octave-shift"]:
                    font = attrs["octave-shift"]["font"]
            data["direction"] = directions.OctaveShift(
                type=l_type,
                amount=amount,
                font=font)

        if tags[-1] == "wavy-line":
            data["direction"] = directions.WavyLine(type=l_type)
        if tags[-1] == "pedal":
            line = None
            if "pedal" in attrs:
                if "line" in attrs["pedal"]:
                    line = YesNoToBool(attrs["pedal"]["line"])
            data["direction"] = directions.Pedal(line=line, type=l_type)
        if tags[-1] == "bracket":
            num = None
            ltype = None
            elength = None
            lineend = None
            if "bracket" in attrs:
                if "number" in attrs["bracket"]:
                    num = int(attrs["bracket"]["number"])
                if "line-type" in attrs["bracket"]:
                    ltype = attrs["bracket"]["line-type"]
                if "end-length" in attrs["bracket"]:
                    elength = int(attrs["bracket"]["end-length"])
                if "line-end" in attrs["bracket"]:
                    lineend = attrs["bracket"]["line-end"]
            data["direction"] = directions.Bracket(
                lineEnd=lineend,
                elength=elength,
                type=l_type,
                ltype=ltype,
                number=num)
    HandleRepeatMarking(tags, attrs, chars, piece, data)

    return return_val


def HandleRepeatMarking(tags, attrs, chars, piece, data):
    global last_note
    if "direction" in tags or "forward" in tags:
        if tags[-1] == "voice":
            data["voice"] = int(chars["voice"])
        measure = None
        part_id = helpers.GetID(attrs, "part", "id")
        measure_id = IdAsInt(helpers.GetID(attrs, "measure", "number"))
        if part_id is not None:
            if measure_id is not None:
                measure = piece.getPart(part_id).getMeasure(
                    measure_id,
                    data["staff_id"])

        if measure is not None:
            d_type = None

            if tags[-1] == "segno" or tags[-1] == "coda":
                d_type = tags[-1]
                data["direction"] = directions.RepeatSign(type=d_type)

            if tags[-1] == "sound":
                if "sound" in attrs:
                    if "coda" in attrs["sound"]:
                        measure.coda = attrs["sound"]["coda"]
                    if "dacapo" in attrs["sound"]:
                        measure.dacapo = YesNoToBool(attrs["sound"]["dacapo"])
                    if "dalsegno" in attrs["sound"]:
                        measure.dalsegno = attrs["sound"]["dalsegno"]
                    if "fine" in attrs["sound"]:
                        measure.fine = YesNoToBool(attrs["sound"]["fine"])
                    if "segno" in attrs["sound"]:
                        measure.segno = attrs["sound"]["segno"]
                    if "tocoda" in attrs["sound"]:
                        measure.tocoda = attrs["sound"]["tocoda"]


def handleLyrics(tags, attrs, chars, piece, data):
    if "lyric" in tags:
        if not hasattr(data["note"], "lyrics"):
            data["note"].lyrics = {}
        number = len(data["note"].lyrics)
        if "lyric" in attrs:
            if "number" in attrs["lyric"]:
                number = int(attrs["lyric"]["number"])
        if number not in data["note"].lyrics:
            data["note"].lyrics[number] = directions.Lyric()
        if tags[-1] == "text":
            data["note"].lyrics[number].text = chars["text"]
        if tags[-1] == "syllabic":
            data["note"].lyrics[number].syllabic = chars["syllabic"]


def handleTimeMod(tags, attrs, chars, piece, data):
    if "notations" in tags:
        if tags[-1] == "tuplet":
            type = None
            bracket = None

            if "tuplet" in attrs:
                if "type" in attrs["tuplet"]:
                    type = attrs["tuplet"]["type"]
                if "bracket" in attrs["tuplet"]:
                    bracket = YesNoToBool(attrs["tuplet"]["bracket"])
            tuplet = note.Tuplet(bracket=bracket, type=type)
            data["note"].add_notation(tuplet)
    if "time-modification" in tags:
        if not hasattr(data["note"], "timeMod"):
            data["note"].timeMod = note.TimeModifier()
        if tags[-1] == "actual-notes":
            data["note"].timeMod.actual = int(chars["actual-notes"])
        if tags[-1] == "normal-notes":
            data["note"].timeMod.normal = int(chars["normal-notes"])
    return None


def CheckDynamics(tag):
    return_val = False
    dmark = ["p", "f"]
    if len(tag) == 1 and tag in dmark:
        return_val = True
    elif len(tag) == 2:
        if tag[-1] in dmark:
            if tag[0] == tag[-1] or tag[0] == "m" or tag[0] == "s":
                return_val = True
    if len(tag) > 2:
        val = tag[0]
        if val in dmark:
            for char in tag:
                if char == val:
                    return_val = True
                else:
                    return_val = False
    return return_val
