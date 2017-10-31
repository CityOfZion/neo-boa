from boa.blockchain.vm.Neo.App import AppCall
from boa.blockchain.vm.Neo.Runtime import Notify


def Main():
    """

    :return:
    """
    fibtest = 7

    # the following does not work
    # need the ability to define
    # dynamically called smart contracts
    # which is not currently supported by the VM
#    shash = b'24196a584e2bd4c343148e553a7bca9738ae3b19'
#    res = AppCall(shash, fibtest)

    # this does work
    res = AppCall('24196a584e2bd4c343148e553a7bca9738ae3b19', fibtest)

    print("did fibo!")

    Notify(res)

    output = res + 18

    return output
