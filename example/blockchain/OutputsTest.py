# tested

from boa.interop.Neo.Blockchain import GetTransaction
from boa.interop.Neo.Transaction import *
from boa.interop.Neo.Output import *

NEO = b'\x9b|\xff\xda\xa6t\xbe\xae\x0f\x93\x0e\xbe`\x85\xaf\x90\x93\xe5\xfeV\xb3J\\"\x0c\xcd\xcfn\xfc3o\xc5'
GAS = b'\xe7-(iy\xeel\xb1\xb7\xe6]\xfd\xdf\xb2\xe3\x84\x10\x0b\x8d\x14\x8ewX\xdeB\xe4\x16\x8bqy,`'


def Main(txid):

    tx = GetTransaction(txid)

    res = []

    # we can iterate over an attribute of an object!
    # this is really exciting, but you'd never know it
    for item in tx.Outputs:
        subres = []
        subres.append(item.Value)
        subres.append(item.AssetId)
        subres.append(item.ScriptHash)
        res.append(subres)

    return res
