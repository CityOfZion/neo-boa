from boa.interop.Neo.Runtime import GetTrigger
from boa.interop.Neo.TriggerType import Application, Verification
# from boa.builtins import concat


def Main():

    trigger = GetTrigger()

    return trigger == Application()
