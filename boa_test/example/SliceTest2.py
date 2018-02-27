# tested

from boa.interop.Neo.Runtime import Notify
from boa.builtins import concat


def Main():

    m = bytearray(b'\x01\x02\x03\x04\x05\x06\x07\x08')

    # this is a test to see if slice notation without specifying an end
    # is functional
#    s1 = m[2:] # it is not

    # without specifying beginning it is:
    s2 = m[:4]

    j = 2
    k = 4

    s3 = m[j:k]

    Notify(s3)

    s4 = m[get_slice_start():get_slice_end()]

    Notify(s4)

    ind = [1, 3, 4, 5]

    s6 = m[get_slice_start():ind[2]]

    Notify(s6)

    res = concat(s6, concat(s4, concat(s2, s3)))

    Notify(res)

    return res


def get_slice_start():

    return 1


def get_slice_end():
    return 6
