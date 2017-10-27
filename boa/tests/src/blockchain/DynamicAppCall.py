from boa.blockchain.vm.Neo.App import RegisterAppCall,AppCall
from boa.blockchain.vm.Neo.Runtime import Notify



def Main():

    """

    :return:
    """
    fibtest = 7

    res = AppCall('24196a584e2bd4c343148e553a7bca9738ae3b19', fibtest)


    print("did fibo!")

    Notify(res)

    output = res + 18

    return output
