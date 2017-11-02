
from boa.code.builtins import list, range
from boa.blockchain.vm.Neo.Runtime import Log, Notify


def Main():
    """

    :return:
    """
    mmm = range(2, 14)

    l = mmm[2]

    Notify(l)

    empty = list()

    b = get_thing()
    c = get_items_from_range(mmm, 7)

    k = range(10, 12)

    return l + b + c + k[0]


def get_thing():
    """

    :return:
    """
    return 7


def get_items_from_range(items, index):
    """

    :param items:
    :param index:
    :return:
    """
    return items[index]
