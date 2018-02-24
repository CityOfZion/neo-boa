# tested

from boa.interop.Neo.Action import RegisterAction

Transfer = RegisterAction('transfer_test', 'from', 'to', 'amount')

Refund = RegisterAction('refund', 'to', 'amount')


def Main():

    a = 2

    b = 5

    c = a + b

    Transfer(a, b, c)

    to = 'me'
    amount = 52

    Refund(to, amount)

    return c
