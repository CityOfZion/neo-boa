from boa.blockchain.vm.Neo.Blockchain import GetHeader, GetBlock
from boa.blockchain.vm.Neo.Runtime import Notify
from boa.blockchain.vm.Neo.Header import GetTimestamp
from boa.blockchain.vm.Neo.Block import GetTransactions


def Main():
    """

    :return:
    """
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
