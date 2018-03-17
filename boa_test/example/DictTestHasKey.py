# tested

from boa.builtins import has_key


def Main():

    d = {
        'a': 1,
        'b': 4,
    }

    result = 0

    if has_key(d, 'a'):
        result += 2

    if not d.has_key('j'):
        result += 3

    if 'b' in d:

        print("b i si in d:")
        result += 17
    else:

        print("b not in d")

    return result  # should be 22
