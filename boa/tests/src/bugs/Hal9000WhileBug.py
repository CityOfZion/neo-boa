from boa.blockchain.vm.Neo.Runtime import GetTrigger
from boa.blockchain.vm.Neo.TriggerType import Application, Verification
from boa.code.builtins import substr


def Main(bytes):

    trigger = GetTrigger()

    if trigger == Verification():
        print("Verification!")
        return False

    elif trigger == Application():
        print("Application!")
        i = 0
        l = len(bytes)
        while i < l:
            c = substr(bytes, i, 1)
            i = i + 1
            if c == 0:
                print("Null")
            else:
                print("Not null")
                return True
