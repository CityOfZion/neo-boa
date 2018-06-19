from boa.interop.Neo.Enumerator import *


def Main(testNum):

    items = [1, 2, 3, 5, 9, 14]

    vals = EnumeratorCreate(items)

    if testNum == 1:

        while EnumeratorNext(vals):

            print("next!")

        print("ok done")

        return True

    if testNum == 2:

        ret = []
        while EnumeratorNext(vals):
            ret.append(vals.Value)

        return ret

    if testNum == 3:
        ret = []
        vals = enumerate(items)

        while EnumeratorNext(vals):
            ret.append(vals.Value)

        return ret

    if testNum == 4:

        items2 = ['a', 'b', 'd', 'f']

        enum2 = EnumeratorCreate(items2)

        doublenumerator = EnumeratorConcat(vals, enum2)

        ret = []

        while EnumeratorNext(doublenumerator):
            ret.append(doublenumerator.Value)
        return ret

    if testNum == 5:

        count = 0
        while next(vals):
            count += 1
        return count

    if testNum == 6:

        myenum = enumerate(items)
        count = 0
        while myenum.next():
            count += 1
        return count

    return False
