from museparse.elements import directions, part
from museparse.input import mxmlparser
from tests.testHandlers import testclass


class testHandleDirections(testclass.TestClass):

    def setUp(self):
        testclass.TestClass.setUp(self)
        self.tags.append("direction")
        self.handler = mxmlparser.HandleDirections
        self.piece.addPart(part.Part(), "P1")
        self.piece.getPart("P1").addEmptyMeasure(1, 1)
        self.measure = self.piece.getPart("P1").getMeasure(1, 1)
        self.attrs["measure"] = {"number": "1"}
        self.attrs["part"] = {"id": "P1"}
        self.data = {"note": None, "direction": None, "expression": None}
        self.data["staff_id"] = 1

    def testNoTags(self):
        self.tags.remove("direction")
        self.assertEqual(
            None,
            self.handler(
                self.tags,
                self.attrs,
                self.chars,
                self.piece,
                self.data))

    def testIrrelevantTags(self):
        self.tags.remove("direction")
        self.tags.append("hello")
        self.assertEqual(
            None,
            self.handler(
                self.tags,
                self.attrs,
                self.chars,
                self.piece,
                self.data))

    def testDirectionAttribTag(self):
        self.tags.append("words")
        self.attrs["direction"] = {"placement": "above"}
        self.chars["words"] = "sup"
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)

        self.assertEqual("above", self.data["direction"].placement)

    def testDirectionTag(self):
        self.tags.append("words")
        self.chars["words"] = "hello, world"
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)

        self.assertIsInstance(self.data["direction"], directions.Direction)
        self.assertEqual("hello, world", self.data["direction"].text)

    def testWordsWithFontSizeAttrib(self):
        self.tags.append("words")
        self.chars["words"] = "hello, world"
        self.attrs["words"] = {"font-size": "6.5"}
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)

        self.assertTrue(hasattr(self.data["direction"], "size"))
        self.assertEqual("6.5", self.data["direction"].size)

    def testWordsWithFontFamAttrib(self):
        self.tags.append("words")
        self.chars["words"] = "hello, world"
        self.attrs["words"] = {"font-family": "times"}
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)

        self.assertTrue(hasattr(self.data["direction"], "font"))
        self.assertEqual("times", self.data["direction"].font)

    def testWordsWithBothAttribs(self):
        self.tags.append("words")
        self.chars["words"] = "hello, world"
        self.attrs["words"] = {"font-family": "times", "font-size": "6.2"}
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)

        self.assertEqual("times", self.data["direction"].font)
        self.assertEqual("6.2", self.data["direction"].size)

    def testOctaveShift(self):
        self.tags.append("octave-shift")
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)

        self.assertIsInstance(self.data["direction"], directions.OctaveShift)

    def testOctaveShiftType(self):
        self.tags.append("octave-shift")
        self.attrs["octave-shift"] = {"type": "down"}
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)

        self.assertTrue(hasattr(self.data["direction"], "type"))

    def testOctaveShiftAmount(self):
        self.tags.append("octave-shift")
        self.attrs["octave-shift"] = {"size": "8"}
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)

        self.assertTrue(hasattr(self.data["direction"], "amount"))
        self.assertEqual(8, self.data["direction"].amount)

    def testWavyLine(self):
        self.tags.append("wavy-line")
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)

        self.assertIsInstance(self.data["direction"], directions.WavyLine)

    def testWavyLineType(self):
        self.tags.append("wavy-line")
        self.attrs["wavy-line"] = {"type": "start"}
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)

        self.assertEqual("start", self.data["direction"].type)

    def testPedal(self):
        self.tags.append("pedal")
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)

        self.assertIsInstance(self.data["direction"], directions.Pedal)

    def testPedalLine(self):
        self.tags.append("pedal")
        self.attrs["pedal"] = {"line": "yes"}
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)

        self.assertEqual(True, self.data["direction"].line)

    def testPedalLineType(self):
        self.tags.append("pedal")
        self.attrs["pedal"] = {"type": "start"}
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)

        self.assertEqual("start", self.data["direction"].type)

    def testBracket(self):
        self.tags.append("bracket")
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)
        self.assertIsInstance(self.data["direction"], directions.Bracket)

    def testBracketType(self):
        self.tags.append("bracket")
        self.attrs["bracket"] = {"type": "start"}
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)

        self.assertEqual("start", self.data["direction"].type)

    def testBracketNumber(self):
        self.tags.append("bracket")
        self.attrs["bracket"] = {"number": "1"}
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)

        self.assertEqual(1, self.data["direction"].number)

    def testBracketLineEnd(self):
        self.tags.append("bracket")
        self.attrs["bracket"] = {"line-end": "none"}
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)

        self.assertEqual("none", self.data["direction"].lineEnd)

    def testBracketEndLength(self):
        self.tags.append("bracket")
        self.attrs["bracket"] = {"end-length": "15"}
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)

        self.assertEqual(15, self.data["direction"].endLength)

    def testBracketLineType(self):
        self.tags.append("bracket")
        self.attrs["bracket"] = {"line-type": "solid"}
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)

        self.assertEqual("solid", self.data["direction"].lineType)


class testMetronome(testHandleDirections):

    def setUp(self):
        testHandleDirections.setUp(self)
        self.tags.append("metronome")

    def testText(self):
        self.tags.remove("metronome")
        self.tags.append("words")
        self.chars["words"] = "hello"
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)
        self.tags.append("metronome")
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)
        self.assertEqual(self.data["direction"].text, "hello")
        self.assertIsInstance(self.data["direction"], directions.Metronome)

    def testMetronomeBeatUnitTag(self):
        self.tags.append("beat-unit")
        self.chars["beat-unit"] = "quarter"
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)

        self.assertTrue(hasattr(self.data["direction"], "beat"))
        self.assertEqual("quarter", self.data["direction"].beat)

    def testMetronome2BeatUnitTags(self):
        self.tags.append("beat-unit")
        self.chars["beat-unit"] = "quarter"
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)
        self.tags.append("beat-unit")
        self.chars["beat-unit"] = "half"
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)
        self.assertTrue(hasattr(self.data["direction"], "beat"))
        self.assertEqual("quarter", self.data["direction"].beat)

    def testMetronome2BeatUnitSecondValueTags(self):
        self.tags.append("beat-unit")
        self.chars["beat-unit"] = "quarter"
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)
        self.tags.append("beat-unit")
        self.chars["beat-unit"] = "half"
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)
        self.assertTrue(hasattr(self.data["direction"], "secondBeat"))
        self.assertEqual("half", self.data["direction"].secondBeat)

    def testBeatUnitWithFontAttrib(self):
        self.tags.append("beat-unit")
        self.chars["beat-unit"] = "quarter"
        self.attrs["metronome"] = {"font-family": "times"}
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)

        self.assertTrue(hasattr(self.data["direction"], "beat"))
        self.assertEqual("quarter", self.data["direction"].beat)
        self.assertTrue(hasattr(self.data["direction"], "font"))
        self.assertEqual("times", self.data["direction"].font)

    def testBeatUnitWithFontSizeAttrib(self):
        self.tags.append("beat-unit")
        self.chars["beat-unit"] = "quarter"
        self.attrs["metronome"] = {"font-size": "6.5"}
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)

        self.assertTrue(hasattr(self.data["direction"], "beat"))
        self.assertEqual("quarter", self.data["direction"].beat)
        self.assertTrue(hasattr(self.data["direction"], "size"))
        self.assertEqual("6.5", self.data["direction"].size)

    def testBeatUnitWithFontAttrib(self):
        self.tags.append("beat-unit")
        self.chars["beat-unit"] = "quarter"
        self.attrs["metronome"] = {"parentheses": "yes"}
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)

        self.assertTrue(hasattr(self.data["direction"], "beat"))
        self.assertEqual("quarter", self.data["direction"].beat)
        self.assertTrue(hasattr(self.data["direction"], "parentheses"))
        self.assertEqual(True, self.data["direction"].parentheses)

    def testBeatUnitAllAttribs(self):
        self.tags.append("beat-unit")
        self.chars["beat-unit"] = "quarter"
        self.attrs["metronome"] = {
            "font-family": "times",
            "font-size": "6.5",
            "parentheses": "yes"}
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)

        self.assertTrue(hasattr(self.data["direction"], "beat"))
        self.assertEqual("quarter", self.data["direction"].beat)
        self.assertTrue(hasattr(self.data["direction"], "font"))
        self.assertEqual("times", self.data["direction"].font)
        self.assertTrue(hasattr(self.data["direction"], "size"))
        self.assertEqual("6.5", self.data["direction"].size)
        self.assertTrue(hasattr(self.data["direction"], "parentheses"))
        self.assertEqual(True, self.data["direction"].parentheses)

    def testPerMinuteTag(self):
        self.tags.append("per-minute")
        self.chars["per-minute"] = "85"
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)
        self.assertIsInstance(self.data["direction"], directions.Metronome)
        self.assertTrue(hasattr(self.data["direction"], "min"))
        self.assertEqual("85", self.data["direction"].min)

    def testPerMinuteFontFamAttrib(self):
        self.tags.append("per-minute")
        self.chars["per-minute"] = "85"
        self.attrs["metronome"] = {"font-family": "times"}
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)

        self.assertTrue(hasattr(self.data["direction"], "font"))
        self.assertEqual("times", self.data["direction"].font)

    def testPerMinuteFontSizeAttrib(self):
        self.tags.append("per-minute")
        self.chars["per-minute"] = "85"
        self.attrs["metronome"] = {"font-size": "6.5"}
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)

        self.assertTrue(hasattr(self.data["direction"], "size"))
        self.assertEqual(6.5, self.data["direction"].size)

    def testPerMinuteParenthesesAttrib(self):
        self.tags.append("per-minute")
        self.chars["per-minute"] = "85"
        self.attrs["metronome"] = {"parentheses": "yes"}
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)

        self.assertTrue(hasattr(self.data["direction"], "parentheses"))
        self.assertTrue(self.data["direction"].parentheses)

    def testPerMinuteAllAttribs(self):
        self.tags.append("per-minute")
        self.chars["per-minute"] = "85"
        self.attrs["metronome"] = {"parentheses": "yes",
                                   "font-size": "6.5",
                                   "font-family": "times"}
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)

        self.assertTrue(hasattr(self.data["direction"], "parentheses"))
        self.assertTrue(self.data["direction"].parentheses)
        self.assertTrue(hasattr(self.data["direction"], "size"))
        self.assertEqual(6.5, self.data["direction"].size)
        self.assertTrue(hasattr(self.data["direction"], "font"))
        self.assertEqual("times", self.data["direction"].font)


class testDynamicsAndSound(testHandleDirections):

    def tearDown(self):
        self.data["expression"] = None

    def testDynamicTag(self):
        self.tags.append("dynamics")
        self.tags.append("p")
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)
        self.assertIsInstance(self.data["expression"], directions.Dynamic)
        self.assertEqual("p", self.data["expression"].mark)

    def testDynamicTagOther(self):
        self.tags.append("dynamics")
        self.tags.append("other-dynamics")
        self.chars["other-dynamics"] = "other"
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)
        self.assertIsInstance(self.data["expression"], directions.Dynamic)
        self.assertEqual("other", self.data["expression"].text)

    def testSoundTag(self):
        self.tags.append("sound")
        self.assertEqual(
            1,
            self.handler(
                self.tags,
                self.attrs,
                self.chars,
                self.piece,
                self.data))

    def testSoundDynamicAttr(self):
        self.tags.append("sound")
        self.attrs["sound"] = {"dynamics": "80"}
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)

        self.assertTrue(hasattr(self.measure, "volume"))
        self.assertEqual("80", self.measure.volume)

    def testSoundTempoAttr(self):
        self.tags.append("sound")
        self.attrs["sound"] = {"tempo": "80"}
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)

        self.assertTrue(hasattr(self.measure, "tempo"))
        self.assertEqual("80", self.measure.tempo)

    def testSoundAttrs(self):
        self.tags.append("sound")
        self.attrs["sound"] = {"dynamics": "60", "tempo": "50"}
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)

        self.assertTrue(hasattr(self.measure, "tempo"))
        self.assertEqual("50", self.measure.tempo)
        self.assertTrue(hasattr(self.measure, "volume"))
        self.assertEqual("60", self.measure.volume)

    def testWedgeTag(self):
        self.tags.append("wedge")
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)

        self.assertIsInstance(self.data["expression"], directions.Wedge)

    def testWedgeVal(self):
        self.tags.append("wedge")
        self.attrs["wedge"] = {"type": "crescendo"}
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)

        self.assertTrue(hasattr(self.data["expression"], "type"))
        self.assertEqual("crescendo", self.data["expression"].type)
