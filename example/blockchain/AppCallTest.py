from boa.interop.Neo.App import RegisterAppCall
from boa.interop.Neo.Runtime import Notify

# Fibo = RegisterAppCall('24196a584e2bd4c343148e553a7bca9738ae3b19', intval=0)

AddContract = RegisterAppCall('d724c4191f83cee8d3c84e5d5bd91a054a9867d0', 'a', 'b')


def Main(a):

    test = 7

    res = AddContract(test, a)

    print("did add")

    Notify(res)

    output = res + 1

    return output
