from museparse.tests.testLilyMethods.lily import Lily
from museparse.classes.ObjectHierarchy.ItemClasses import Meter


class testTimeSig(Lily):

    def setUp(self):
        self.item = Meter.Meter()
        self.lilystring = "\\time 4/4"


class testTimeSigBeat(Lily):

    def setUp(self):
        self.item = Meter.Meter(beats=2)
        self.lilystring = "\\time 2/4"


class testTimeSigType(Lily):

    def setUp(self):
        self.item = Meter.Meter(type=2)
        self.lilystring = "\\time 2/2"


class testTimeSigBeatAndType(Lily):

    def setUp(self):
        self.item = Meter.Meter(type=8, beats=6)
        self.lilystring = "\\time 6/8"


class testTimeSigSingleNumber(Lily):

    def setUp(self):
        self.item = Meter.Meter(type=8, beats=6, style="single-number")
        self.lilystring = "\n\once \override Staff.TimeSignature.style = #'single-digit\n\\time 6/8"
