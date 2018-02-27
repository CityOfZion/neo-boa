
from boa.builtins import concat


def Main(ba1, ba2):

    m = ba2[1:2]  # but you can do this instead

    # strings and byte arrays work the same
    mystr = 'staoheustnau'

    # this will not work
    # m = mystr[3]

    # but this will
    m = mystr[3:5]

    #
    m = ba1[1:len(ba1)]

    return concat(m, concat(mystr, ba2))
