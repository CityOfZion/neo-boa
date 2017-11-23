from boa.blockchain.vm.Neo.Runtime import Notify

from .stuff.things import Awesome


def Main(a):

    # create an instance
    m = Awesome()

    q = 1
    name = m.awesome_name()

    Notify(name)

    return q  # should be 2
