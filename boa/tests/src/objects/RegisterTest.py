from boa.blockchain.vm.Neo.Action import RegisterAction


call_event = RegisterAction('event', 'arg1', 'arg2')


def Main():

    m = 3

    b = 8

    call_event(m, b)

    return 3
