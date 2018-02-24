# tested

from boa.builtins import range


def Main():

    rangestart = 2
    count = 0

    for i in range(rangestart, getrangeend()):
        count += 1

    return count


def getrangeend():
    return 8
