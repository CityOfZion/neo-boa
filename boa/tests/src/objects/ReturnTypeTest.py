from boa.blockchain.vm.Neo.Runtime import Notify

from .stuff.things import Awesome



def Main(a):



    b = CreateAwesome()

    q = b.mycount

    return q # should be 2



def CreateAwesome() -> Awesome:

    a = Awesome()
    return a

