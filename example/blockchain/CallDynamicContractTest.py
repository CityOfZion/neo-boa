from boa.interop.Neo.App import RegisterAppCall
from boa.interop.Neo.Runtime import Notify


DynamicContract = RegisterAppCall('f35ab70fab7c32683cc013e3f3ec434454b84553', 'a')


def Main(a):

    res = DynamicContract(a)

    print("did add")

    Notify(res)

    output = res + 1

    return output
