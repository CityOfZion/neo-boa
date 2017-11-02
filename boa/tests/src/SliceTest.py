from boa.blockchain.vm.Neo.Runtime import Notify


def Main():

    m = bytearray(b'\x01\x02\x03\x04\x05\x06\x07\x08')

    # this is a test to see if slice notation without specifying an end
    # is functional
    s1 = m[4:]

    Notify(s1)  # should be b'\x05\x06\x07\x08'

    q = 2

    a = 1

    # this is a test to see if a bunch of different stuff works
    s2 = m[a + q - 1:get_slice_end() - 1]

    Notify(s2)  # expected result should be b'\x03\x04'

    return s1


def get_slice_end():

    return 5
