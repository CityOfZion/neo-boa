
def Main():
    """

    :return:
    """
    a = 1

    b = 2

    c = stuff()

    d = stuff2()

    e = stuff8()

    f = blah()

    h = prevcall()

    return a + c + d + f + b + h


def stuff():
    """

    :return:
    """
    a = 4

    b = 2

    return a + b


def stuff2():
    """

    :return:
    """
    a = 8

    j = 10

    return j - a


def prevcall():
    """

    :return:
    """
    return stuff()


def stuff8():
    """

    :return:
    """
    q = 'hello'

    return q


def blah():
    """

    :return:
    """
    return 1 + 8
