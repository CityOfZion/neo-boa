from boa.code.builtins import concat
from boa.blockchain.vm.Neo.Runtime import Notify


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
