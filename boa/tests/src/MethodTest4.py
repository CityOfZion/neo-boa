

def Main():
    """

    :return:
    """
    a = 1

    b = 10

    c = 20

    d = add(a, b, 10)

    d2 = add(d, d, d)

    return d2


def add(a, b, c):
    """

    :param a:
    :param b:
    :param c:
    :return:
    """
    result = a + b + c

    return result
