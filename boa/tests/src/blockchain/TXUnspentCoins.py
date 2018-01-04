from boa.blockchain.vm.Neo.Transaction import *
from boa.blockchain.vm.Neo.Blockchain import GetTransaction
from boa.blockchain.vm.Neo.Runtime import Notify
from boa.blockchain.vm.Neo.Output import GetValue, GetScriptHash


def Main(txhash):

    tx = GetTransaction(txhash)

    unspent = tx.UnspentCoins

    count = 0
    for uns in unspent:
        val = uns.Value
        Notify(val)

    return tx.Hash
