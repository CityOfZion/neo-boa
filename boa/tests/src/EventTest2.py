
from boa.blockchain.vm.Neo.Action import RegisterAction


Transfer = RegisterAction('transfer', 'from', 'to', 'amount')

Refund = RegisterAction('refund', 'to', 'amount')


def Main():
    """

    :return:
    """
    a = 2

    b = 5

    c = a + b

    Transfer(a, b, c)

    to = 'me'
    amount = 52

    Refund(to, amount)

    d = Second(a)

    return d + 3


def Second(a):
    """

    :param a:
    :return:
    """
    j = 'hello'
    b = 'goodbye'

    Transfer(a, j, b)

    return 2
