from boa.blockchain.vm.Neo.Runtime import Notify

from .stuff.things import Awesome, MoreAwesome


def Main(a):

    # this should mess things up
    k = Awesome()

    m = what()  # type:MoreAwesome

    collection = [k, m, 5]

    k2 = collection[0]  # type:Awesome

    k2count = k2.mycount

    m2 = collection[1]  # type:MoreAwesome

    k2count += m2.intval

    j2 = collection[2]  # type:int

    Notify(k2count)

    Notify(j2)

    return 1


def what():

    q = MoreAwesome()

    return q
