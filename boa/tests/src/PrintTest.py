
from boa.code.builtins import list, range
from boa.blockchain.vm.Neo.Runtime import Log, Notify


def Main():
    """

    :return:
    """
    print("holla?")  # using pythonic print(), this is tranlated to Neo.Runtime.Log
    start = 4
    stop = 9

    r = range(start, stop)

    # using built in Neo.Runtime.Log( this is the same as print(message) )
    Log("hellllllllloo")

    # using the Neo.Runtime.Notify ( this is for logging variables... )
    Notify(start)

    l = list(length=stop)

    l[3] = 17

    b = r[3]
    print("hullo")

    return b
