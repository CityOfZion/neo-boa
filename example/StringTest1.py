from boa.code.builtins import concat
from boa.interop.Neo.Runtime import Notify


def Main(a, b):
    """

    :param a:
    :param b:
    :return:
    """
    c = concat(a, b)

    Notify(c)

    if c == 'hellogoodbye':

        return 3

    return 1
