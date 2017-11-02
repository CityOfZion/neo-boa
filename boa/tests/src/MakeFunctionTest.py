

def Main():
    """

    :return:
    """

    def h(a, b):
        """

        :param a:
        :param b:
        :return:
        """
        return a + b

    k = h(1, 8)

    def q(a, b):

        # this will not work at the moment... not sure why you
        # would want to do this
        # l = h(3, 4)
        """

        :param a:
        :param b:
        :return:
        """
        return a - b

    t = q(10, 3)

    return k + mmm() + t


def mmm():
    """

    :return:
    """
    return 9
