
from boa.code.builtins import list
from boa.blockchain.vm.Neo.Runtime import Notify


def Main():
    """

    :return:
    """
    start = 4
    stop = 9  # int

#    out = [10,2, 3, 4, 6, 7]

    length = stop - start

    out = list(length=length)

    index = 0
    orig_start = start

    # this causes an execution error
    st = stuff(start, stop)

    while start < stop:
        val = index + orig_start
        out[index] = val
        index = index + 1
        start = orig_start + index


    return out[4]


def stuff(a, b):
    """

    :param a:
    :param b:
    :return:
    """
    out = a + b
    return out
