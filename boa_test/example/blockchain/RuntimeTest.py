# tested

from boa.interop.Neo.Runtime import *


def Main(operation, arg):

    if operation == 'get_trigger':
        return GetTrigger()

    elif operation == 'check_witness':
        return CheckWitness(arg)

    elif operation == 'get_time':
        return GetTime()

    elif operation == 'log':
        Log(arg)
        return True

    elif operation == 'notify':
        Notify(arg)
        return True

    return 'unknown'
