from boa.blockchain.vm.Neo.Action import RegisterAction
from boa.blockchain.vm.Neo.Runtime import Notify


OnThing = RegisterAction('blah','bloop','bleep')


def Main():
    """

    :return:
    """
    ename = 'thing'
    arg1 = 2
    arg2 = 4

    OnThing(ename, arg1, arg2)


    return arg1
