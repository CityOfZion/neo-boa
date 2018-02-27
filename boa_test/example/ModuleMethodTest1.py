
from boa.builtins import sha1

MYSHA = sha1('abc')


def Main():

    m = 3

    j2 = sha1('abc')

    j3 = MYSHA

#    print(j2)

    return j2 == j3
