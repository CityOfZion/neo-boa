
def Main(a, b, c, d):
    """

    :param a:
    :param b:
    :param c:
    :param d:
    :return:
    """
    m = 0

    if a > b:

        if c > d:

            m = 3

        else:

            if b > c:

                return 8

            else:

                return 10

    else:

        if c > d:

            m = 1

        else:

            if b < c:

                return 11

            else:

                m = 22

    return m
