from boa.blockchain.vm.Neo.Runtime import Notify


def Main():
    """

    :return:
    """
    items = [1, 3]

#    j = 0
#    for i in items:
#        j += i
#    i2 = [i+1 if i > 0 else i + 5 for i in items]

#    m = 0
    [Notify(i) for i in items]  # this is not working

    m = 3

    return m
