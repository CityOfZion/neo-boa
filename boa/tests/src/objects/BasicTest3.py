from boa.blockchain.vm.Neo.Runtime import Notify

from .stuff.things import MoreAwesome


def Main(a):

    # create an instance
    m = MoreAwesome()

    q = 2

    m.intval = 13

    result = m.add_thirteen_to_this(q)

    Notify(result)  # should be fifteen

    mult = m.multiply_nums(3, 7)

    Notify(mult)

    atimes42 = m.multiply_by_awesome(2)

    Notify(atimes42)

    return result  # should be 15
