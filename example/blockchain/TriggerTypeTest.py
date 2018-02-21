from boa.interop.Neo.TriggerType import Application, Verification

from boa.interop.Neo.Runtime import Log, GetTrigger, Notify


def Main():

    trigger = GetTrigger()

    Notify(trigger)

    if trigger == Application():
        print("application!")

    elif trigger == Verification():
        print("verification!")

    k = 10

    print("hello")

    return k
