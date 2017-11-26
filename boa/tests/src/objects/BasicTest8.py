from boa.blockchain.vm.Neo.Runtime import Notify

from .stuff.things import Awesome, MoreAwesome


def Main(a):

    # create an instance
    m1 = MoreAwesome()

    inpt = 12

    result = m1.add_thirteen_to_this(43)

    result = m1.mmmm(67)

    Notify(result)

    return result
