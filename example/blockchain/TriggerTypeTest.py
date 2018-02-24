# tested

from boa.interop.Neo.TriggerType import Application, Verification
from boa.interop.Neo.Runtime import GetTrigger


def Main(arg):

    if arg == 1:
        return Application()

    elif arg == 2:
        return Verification()

    elif arg == 3:

        if GetTrigger() == Application():
            return b'\x20'

    return -1
