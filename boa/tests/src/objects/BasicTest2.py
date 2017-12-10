from boa.blockchain.vm.Neo.Runtime import Notify

from .stuff.things import Awesome


def Main(a):

    # create an instance
    m = Awesome()

    # passing an item to a method doesn't work
    q = second(m, 8, m)

    return q  # should be 2


def second(item: Awesome, num: int, item2: Awesome):

    j = item.mycount

    total = j + num + item2.mycount

    Notify(total)

    return total
