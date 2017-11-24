from boa.blockchain.vm.Neo.Runtime import Notify

from .stuff.things import Awesome, MoreAwesome


def Main(a):

    # create an instance
    m1 = Awesome()
    m1.mycount = a

    m2 = Awesome()

    mm = MoreAwesome()

#       this works ok
    total = mm.accept_two_awesomes(m1, m2)
    Notify(total)

    # testing whether you can use more than one set of `LOAD_ATTR` in one operation
    total = m1.mycount + m2.mycount + m2.mycount
    total2 = 3 + m1.mycount
    total4 = m1.mycount + 3

    return total  # should be 53
