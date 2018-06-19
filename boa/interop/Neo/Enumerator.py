
class Enumerator:

    @property
    def Value(self):
        return EnumeratorValue(self)

    def Next(self):
        return EnumeratorNext(self)


def EnumeratorCreate(items):
    pass


def EnumeratorNext(enumerator):
    pass


def EnumeratorValue(enumerator):
    pass


def EnumeratorConcat(enumerator1, enumerator2):
    pass
