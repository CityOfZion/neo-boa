# tested
from boa.builtins import list
from boa.interop.Neo.Runtime import Notify


def Main():

    m = 3

    j = list(length=m)

    j[0] = 3

    j[1] = 2

    q = j[0]

    Notify(q)

    return j
