from boa.interop.Neo.Blockchain import GetHeader, GetBlock
from boa.interop.Neo.Runtime import Notify
from boa.interop.Neo.Header import GetTimestamp
from boa.interop.Neo.Block import GetTransactions


def Main():

    header = GetHeader(1234)

    m2 = header.Timestamp + header.Timestamp

    Notify(m2)

    bheight = 32

    block = GetBlock(bheight)

    Notify(block)

    tx = block.Transactions[0]

    Notify(tx.Hash)

#    Notify(tx)
#    tx = block.Transactions[0] #  this doesnt seem to work
#    txhash = tx.Hash

#    Notify(txhash)

    return 1
