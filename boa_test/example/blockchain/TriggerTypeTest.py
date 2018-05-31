# tested

from boa.interop.Neo.TriggerType import Application, Verification, ApplicationR, VerificationR
from boa.interop.Neo.Runtime import GetTrigger


def Main(arg):

    if arg == 1:
        return Application()

    elif arg == 2:
        return Verification()

    elif arg == 3:

        if GetTrigger() == Application():
            return b'\x20'

    elif arg == 4:
        return ApplicationR()

    elif arg == 5:
        return VerificationR()

    return -1
