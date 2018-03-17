# tested

from boa.builtins import values, concat
from boa.interop.Neo.Runtime import Notify


def Main():

    j = 10

    d = {
        'a': 1,
        'b': 4,
        4: 22,
        'm': j,
    }

    output = 0
    for item in values(d):
        output += item

    d2 = {
        't': 5,
        'r': 6,
        's': 7
    }

    for item in d2.values():

        output += item

    return output


def mymethod(a, b):

    return a + b
