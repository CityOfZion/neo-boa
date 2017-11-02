from boa.blockchain.vm.Neo.App import RegisterAppCall
from boa.blockchain.vm.Neo.Runtime import Notify

Fibo = RegisterAppCall('24196a584e2bd4c343148e553a7bca9738ae3b19', intval=0)


def Main():
    """

    :return:
    """
    fibtest = 7

    res = Fibo(fibtest)

    print("did fibo!")

    Notify(res)

    output = res + 18

    return output
