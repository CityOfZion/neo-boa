from boa.blockchain.vm.Neo.Runtime import Notify

from .stuff.things import Awesome, MoreAwesome


def Main(a):

    b = CreateAwesome()

    q = b.mycount

    m = MoreAwesome()

    j = m.instantiate_awesome(7)  # type:Awesome

    Notify(j.mycount)

    return q  # should be 25


def CreateAwesome() -> Awesome:

    a = Awesome()
    return a
