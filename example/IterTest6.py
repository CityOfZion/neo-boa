# tested

from boa.builtins import range


def Main():

    items = range(0, 10)

    count = 0

    for i in items:
        count += 1

    return count
