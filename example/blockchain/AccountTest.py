# tested

from boa.interop.Neo.Blockchain import GetAccount
from boa.interop.Neo.Account import *

NEO = b'\x9b|\xff\xda\xa6t\xbe\xae\x0f\x93\x0e\xbe`\x85\xaf\x90\x93\xe5\xfeV\xb3J\\"\x0c\xcd\xcfn\xfc3o\xc5'
GAS = b'\xe7-(iy\xeel\xb1\xb7\xe6]\xfd\xdf\xb2\xe3\x84\x10\x0b\x8d\x14\x8ewX\xdeB\xe4\x16\x8bqy,`'


def Main(operation, acct):

    account = GetAccount(acct)

    if not account:
        return False

    if operation == 'get_hash':
        return account.ScriptHash

    elif operation == 'get_votes':
        return account.Votes

    elif operation == 'get_balance_gas':
        return GetBalance(account, GAS)

    elif operation == 'get_balance_neo':
        return GetBalance(account, NEO)

    return 'unknown operation'
