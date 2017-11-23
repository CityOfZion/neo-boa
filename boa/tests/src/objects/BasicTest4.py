from boa.blockchain.vm.Neo.Runtime import Notify

from .stuff.things import MoreAwesome, Awesome


def Main(a):

    # create an instance
    moar = MoreAwesome()

    awe = Awesome()

    count = moar.intval + 3

    count += awe.mycount

    # This does not work right now?
    # count2 = moar.intval + awe.mycount

    j = moar.multiply_nums(count, 3)

    Notify(j)

    thing = moar.do_something_with_awesome(awe)

    Notify(thing)

    mm = moar.make_awesome()

    Notify(mm)

    # this works
    r = moar.multiply_nums(awe.mycount, 4)

    # this doesnt work
    # r = moar.multiply_nums(awe.mycount, awe.mycount)

    r = moar.multiply_nums(5, awe.mycount)

    Notify(r)

    return count
