from boa.interop.Neo.Iterator import *


def Main(testNum):

    items = {
        'a': 1,
        'c': 4,
        'f': 13
    }

    vals = IterCreate(items)

    if testNum == 1:

        while IterNext(vals):

            print("next!")

        print("ok done")

        return True

    if testNum == 2:
        count = 0
        while next(vals):
            count += 1
        return count

    if testNum == 3:
        i = iter(items)
        keys = []
        while next(i):
            keys.append(i.Key)

        return keys

    if testNum == 4:
        i = iter(items)
        values = []
        while next(i):
            values.append(i.Value)

        return values

    if testNum == 5:
        count = 0
        while vals.next():
            count += 1
        return count

    if testNum == 6:
        keys = []
        while vals.Keys.next():
            keys.append(vals.Value)
        return keys

    return False
