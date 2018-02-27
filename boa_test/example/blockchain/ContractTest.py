# tested

from boa.interop.Neo.Blockchain import GetContract
from boa.interop.Neo.Contract import *


def Main(operation, ctr):

    if operation == 'get_contract':
        return GetContract(ctr)

    elif operation == 'get_script':
        return GetContract(ctr).Script

    elif operation == 'get_storage_context':
        return GetContract(ctr).StorageContext

    elif operation == 'destroy':
        Destroy()
        return True

    return 'unknown operation'
