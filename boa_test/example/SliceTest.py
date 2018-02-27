# tested


def Main():

    m = bytearray(b'\x01\x02\x03\x04\x05\x06\x07\x08')

    # this is a test to see if slice notation without specifying an end
    # is functional
#    s1 = m[2:] # it is not

    # without specifying beginning it is:
    s2 = m[:4]

    return s2
