from museparse.classes.ObjectHierarchy.ItemClasses import Directions, Meta
from museparse.tests.testLilyMethods.lily import Lily


class testMeta(Lily):

    def setUp(self):
        self.item = Meta.Meta()
        self.lilystring = "\header {\n\n}"


class testMetaTitle(Lily):

    def setUp(self):
        self.item = Meta.Meta(title="hello world")
        self.lilystring = "\header {\ntitle = \"hello world\"\n\n}"


class testMetaComposer(Lily):

    def setUp(self):
        self.item = Meta.Meta(composer="Danny Brown")
        self.lilystring = "\header {\ncomposer = \"Danny Brown\"\n\n}"


class testMetaCreds(Lily):

    def setUp(self):
        self.item = Meta.Meta()
        self.item.credits = [Directions.CreditText(text="hello")]
        self.lilystring = "\header {\n\n}\markuplist {\n\\vspace #0.5\n\n\"hello\"  }"
