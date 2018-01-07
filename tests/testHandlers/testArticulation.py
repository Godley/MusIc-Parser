from tests.testHandlers import testclass
from museparse.elements import directions, note, mark, part
from museparse.input import mxmlparser


class testHandleArticulation(testclass.TestClass):

    def setUp(self):
        testclass.TestClass.setUp(self)
        self.piece.addPart(index="P1", item=part.Part())
        self.part = self.piece.getPart("P1")
        self.part.addEmptyMeasure(1, 1)
        measure = self.part.getMeasure(1, 1)
        self.data = {}
        self.data["note"] = note.Note()
        self.note = self.data["note"]
        measure.addNote(self.data["note"])
        self.handler = mxmlparser.handleArticulation
        self.tags.append("articulations")

    def testNoData(self):
        self.tags.remove("articulations")
        self.assertEqual(
            None,
            self.handler(
                self.tags,
                self.attrs,
                self.chars,
                self.piece,
                self.data))

    def testIrrelevant(self):
        self.tags.remove("articulations")
        self.tags.append("what")
        self.assertEqual(
            None,
            self.handler(
                self.tags,
                self.attrs,
                self.chars,
                self.piece,
                self.data))

    def testRelevant(self):
        self.assertEqual(
            1,
            self.handler(
                self.tags,
                self.attrs,
                self.chars,
                self.piece,
                self.data))

    def testArticulationAccentTag(self):
        self.tags.append("accent")
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)
        self.assertIsInstance(self.note.get_notation(-1, "post"), mark.Accent)

    def testArticulationAccentType(self):
        self.tags.append("accent")
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)
        self.assertEqual("-", self.note.get_notation(-1, "post").symbol)

    def testArticulationSaccentTag(self):
        self.tags.append("strong-accent")
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)
        self.assertIsInstance(
            self.note.get_notation(-1, "post"), mark.StrongAccent)

    def testArticulationStrongAccentTag(self):
        self.tags.append("strong-accent")
        self.attrs = {"type": "down"}
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)
        self.assertEqual("V", self.note.get_notation(-1, "post").symbol)

    def testStaccato(self):
        self.tags.append("staccato")
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)
        self.assertIsInstance(self.note.get_notation(-1, "post"), mark.Staccato)

    def testStaccatoSymbol(self):
        self.tags.append("staccato")
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)
        self.assertEqual(".", self.note.get_notation(-1, "post").symbol)

    def testStaccatissimo(self):
        self.tags.append("staccatissimo")
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)
        self.assertIsInstance(
            self.note.get_notation(-1, "post"), mark.Staccatissimo)

    def testStaccatissimoSymbol(self):
        self.tags.append("staccatissimo")
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)
        self.assertEqual("triangle", self.note.get_notation(-1, "post").symbol)

    def testDetachedLegato(self):
        self.tags.append("detached-legato")
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)
        self.assertIsInstance(
            self.note.get_notation(-1, "post"), mark.DetachedLegato)

    def testDetachedLegSymbol(self):
        self.tags.append("detached-legato")
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)
        self.assertEqual("lineDot", self.note.get_notation(-1, "post").symbol)

    def testTenuto(self):
        self.tags.append("tenuto")
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)
        self.assertIsInstance(self.note.get_notation(-1, "post"), mark.Tenuto)

    def testTenutoSymbol(self):
        self.tags.append("tenuto")
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)
        self.assertEqual("line", self.note.get_notation(-1, "post").symbol)


class testLyrics(testclass.TestClass):

    def setUp(self):
        testclass.TestClass.setUp(self)
        self.tags.append("note")
        self.tags.append("lyric")
        self.handler = mxmlparser.handleLyrics
        self.data = {}
        self.data["note"] = note.Note()

    def testLyricCreation(self):
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)
        self.assertTrue(hasattr(self.data["note"], "lyrics"))

    def testLyricNum(self):
        self.attrs["lyric"] = {"number": "1"}
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)
        self.assertTrue(1 in self.data["note"].lyrics.keys())

    def testLyricText(self):
        self.attrs["lyric"] = {"number": "1"}
        self.chars["text"] = "aaah"
        self.tags.append("text")
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)
        self.assertEqual("aaah", self.data["note"].lyrics[1].text)

    def testLyricSyllable(self):
        self.attrs["lyric"] = {"number": "1"}
        self.chars["syllabic"] = "single"
        self.tags.append("syllabic")
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)
        self.assertEqual("single", self.data["note"].lyrics[1].syllabic)


class testFermata(testclass.TestClass):

    def setUp(self):
        testclass.TestClass.setUp(self)
        self.tags.append("fermata")
        self.data = {}
        self.data["note"] = note.Note()
        self.handler = mxmlparser.HandleFermata

    def testFermata(self):
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)
        self.assertIsInstance(
            self.data["note"].get_notation(-1, "post"), mark.Fermata)

    def testFermataType(self):
        self.attrs["fermata"] = {"type": "inverted"}
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)
        self.assertEqual("inverted", self.data[
                         "note"].get_notation(-1, "post").type)

    def testFermataSymbol(self):
        self.chars["fermata"] = "square"
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)
        self.assertEqual("square", self.data[
                         "note"].get_notation(-1, "post").symbol)


class testSlurs(testclass.TestClass):

    def setUp(self):
        testclass.TestClass.setUp(self)
        self.tags.append("note")
        self.tags.append("notations")
        self.handler = mxmlparser.handleOtherNotations
        self.data = {}
        self.data["note"] = note.Note()

    def testNoData(self):
        self.tags.remove("note")
        self.tags.remove("notations")
        self.assertEqual(
            None,
            self.handler(
                self.tags,
                self.attrs,
                self.chars,
                self.piece,
                self.data))

    def testUnrelated(self):
        self.tags.remove("note")
        self.tags.remove("notations")
        self.tags.append("hello")
        self.assertEqual(
            None,
            self.handler(
                self.tags,
                self.attrs,
                self.chars,
                self.piece,
                self.data))

    def testRelated(self):
        self.assertEqual(
            1,
            self.handler(
                self.tags,
                self.attrs,
                self.chars,
                self.piece,
                self.data))

    def testSlur(self):
        self.tags.append("slur")
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)
        self.assertTrue(hasattr(self.data["note"], "slurs"))
        self.assertEqual(directions.Slur, type(self.data["note"].slurs[0]))

    def testSlurWithId(self):
        self.tags.append("slur")
        self.attrs = {"slur": {"number": "1"}}
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)
        self.assertTrue(len(self.data["note"].slurs) == 1)

    def testSlurType(self):
        self.tags.append("slur")
        self.attrs["slur"] = {"type": "start"}
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)
        self.assertTrue(hasattr(self.data["note"].slurs[0], "type"))
        self.assertEqual("start", self.data["note"].slurs[0].type)

    def testTwoSlursOfTheSameIndex(self):
        self.tags.append("slur")
        self.attrs["slur"] = {"number": "1", "type": "start"}
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)
        self.tags.append("slur")
        self.attrs["slur"] = {"number": "1", "type": "stop"}
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)
        self.assertEqual(self.data["note"].slurs[0].type, "start")
        self.assertEqual("stop", self.data["note"].slurs[1].type)


class t(testclass.TestClass):

    def setUp(self):
        testclass.TestClass.setUp(self)
        self.tags.append("note")
        self.tags.append("notations")
        self.handler = mxmlparser.handleOtherNotations
        self.data = {"direction": None}
        self.data["note"] = note.Note()
        self.tags.append("technical")


class testpostnotation(t):

    def testNoData(self):
        self.tags.remove("notations")
        self.tags.remove("note")
        self.tags.remove("technical")
        self.assertIsNone(
            self.handler(
                self.tags,
                self.attrs,
                self.chars,
                self.piece,
                self.data))

    def testIrrelevant(self):
        self.tags.remove("technical")
        self.tags.remove("notations")
        self.tags.remove("note")
        self.tags.append("hello")
        self.assertIsNone(
            self.handler(
                self.tags,
                self.attrs,
                self.chars,
                self.piece,
                self.data))


class testClosedTechnique(t):

    def setUp(self):
        t.setUp(self)
        self.tag = ""

    def testCreated(self):
        self.tags.append(self.tag)
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)
        self.assertIsInstance(
            self.data["note"].GetNotation(-1, "post"), mark.Technique)

    def testTechniqueType(self):
        self.tags.append(self.tag)
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)
        self.assertTrue(
            hasattr(self.data["note"].GetNotation(-1, "post"), "type"))
        self.assertEqual(self.tag, self.data[
                         "note"].GetNotation(-1, "post").type)


class testUpBow(testClosedTechnique):

    def setUp(self):
        testClosedTechnique.setUp(self)
        self.tag = "up-bow"


class testDownBow(testClosedTechnique):

    def setUp(self):
        testClosedTechnique.setUp(self)
        self.tag = "down-bow"


class testSnapPizz(testClosedTechnique):

    def setUp(self):
        testClosedTechnique.setUp(self)
        self.tag = "snap-pizzicato"


class testOpenTechnique(testClosedTechnique):

    def setUp(self):
        t.setUp(self)
        self.tag = ""
        self.value = ""

    def testTechniqueText(self):
        self.tags.append(self.tag)
        self.chars[self.tag] = self.value
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)
        self.assertEqual(self.value, self.data[
                         "note"].GetNotation(-1, "post").symbol)


class testFingering(testOpenTechnique):

    def setUp(self):
        testOpenTechnique.setUp(self)
        self.tag = "fingering"
        self.value = "0"


class testPluck(testOpenTechnique):

    def setUp(self):
        testOpenTechnique.setUp(self)
        self.tag = "pluck"
        self.value = "p"


class testString(testOpenTechnique):

    def setUp(self):
        testOpenTechnique.setUp(self)
        self.tag = "string"
        self.value = "0"


class testBend(t):

    def testBend(self):
        self.tags.append("technical")
        self.tags.append("bend")
        self.tags.append("bend-alter")
        self.chars["bend-alter"] = "6"
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)
        self.assertEqual(6, self.data["note"].GetNotation(-1, "post").value)
