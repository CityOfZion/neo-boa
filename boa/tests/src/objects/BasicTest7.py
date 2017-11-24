from boa.blockchain.vm.Neo.Runtime import Notify

from .stuff.things import Awesome, MoreAwesome


def Main(a):

    # create an instance
    m1 = Awesome()
    m1.mycount = a

    m2 = Awesome()
    m2.mycount = 4 * a

    mm = MoreAwesome()

    res = mm.multiply_nums(m1.mycount, m2.mycount)

    Notify(res)

    return res
