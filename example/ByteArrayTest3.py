
from boa.builtins import concat


def Main():

    m = bytearray(b'\x01\x02')

    j = get_ba()

    return concat(m, j)


def get_ba():

    return bytearray(b'\xaa\xfe')
