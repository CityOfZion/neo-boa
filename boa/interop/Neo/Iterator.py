
class Iterator:

    @property
    def Value(self):
        return IterValue(self)

    @property
    def Values(self):
        return IterValues(self)

    @property
    def Key(self):
        return IterKey(self)

    @property
    def Keys(self):
        return IterKeys(self)

    def Next(self):
        return IterNext(self)


def IterCreate(items):
    pass


def IterNext(items):
    pass


def IterKey(items):
    pass


def IterKeys(items):
    pass


def IterValue(items):
    pass


def IterValues(items):
    pass
