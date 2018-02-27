# tested

from boa.builtins import concat


def Main():

    items = [0, 1, 2]

    items2 = ['a', 'b', 'c', 'd']
    count = 0

    blah = b''

    for i in items:

        for j in items2:

            blah = concat(blah, j)

            count += 1

    blah = concat(blah, count)

    return blah
