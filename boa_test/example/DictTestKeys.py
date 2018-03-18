# tested

from boa.builtins import keys, concat
from boa.interop.Neo.Runtime import Notify


def Main():

    j = 10

    d = {
        'a': 1,
        'b': 4,
        4: 'blah',
        'm': j,
        'z': [1, 3, 4, 5, 'abcd', j],
        'mcalll': mymethod(1, 4)
    }

    output = ''
    for item in keys(d):
        output = concat(output, item)

    d2 = {
        't': 5,
        'r': 6,
        's': 'a'
    }

    for item in d2.keys():

        output = concat(output, item)

    return output


def mymethod(a, b):

    return a + b
