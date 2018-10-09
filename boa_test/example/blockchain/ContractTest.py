# tested

from boa.interop.Neo.Blockchain import GetContract
from boa.interop.Neo.Contract import *


def Main(operation, ctr):
    
    contract = GetContract(ctr)
    
    if operation == 'get_contract':
        return contract

    elif operation == 'get_script':
        return contract.Script

    elif operation == 'get_storage_context':
        return contract.StorageContext

    elif operation == 'destroy':
        Destroy()
        return True

    elif operation == 'is_payable':
        return contract.IsPayable

    return 'unknown operation'
