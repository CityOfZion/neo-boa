from boa.interop.Neo.Runtime import CheckWitness, Notify, GetTrigger
from boa.interop.Neo.TriggerType import Application, Verification

owner = b'^\x88\xdbm\x10O}g\x1a\x86\xe3\xda\xce\xa7#\xff\x1a\x10*\xe4'


def Main(a):

    trigger = GetTrigger()

    if trigger == Verification():

        if not CheckWitness(owner):

            print("not owner!!")
            return False

        return True

    elif trigger == Application():

        print("do some other thing")

        m = 3

        j = a + m

        return j

    return 3
