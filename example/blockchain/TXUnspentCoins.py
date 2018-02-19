from boa.interop.Neo.Transaction import *
from boa.interop.Neo.Blockchain import GetTransaction
from boa.interop.Neo.Runtime import Notify
from boa.interop.Neo.Output import GetValue, GetScriptHash


def Main(txhash):

    tx = GetTransaction(txhash)

    unspent = tx.UnspentCoins

    count = 0
    for uns in unspent:
        val = uns.Value
        Notify(val)

    return tx.Hash
