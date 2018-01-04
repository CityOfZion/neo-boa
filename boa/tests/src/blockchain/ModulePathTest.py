from boa.blockchain.vm.Neo.Runtime import Notify
from boa.blockchain.vm.Neo.Blockchain import GetHeader, GetBlock
from boa.blockchain.vm.Neo.Header import GetTimestamp
from boa.blockchain.vm.Neo.Block import GetTransactions
from boa.blockchain.vm.Neo.Transaction import *

INVOKE_TX_TYPE = b'\xd1'


def Main(block_index):
    """

    :param block_index:
    :return:
    """
    header = GetHeader(block_index)

    print("got block!")

    ts = header.Timestamp

    print("got timestamp")

    block = GetBlock(block_index)

    txlist = block.Transactions

    # @TODO this does not work
#    for tx in block.Transactions

    for tx in txlist:

        type = tx.Type
        hash = tx.Hash
        Notify(type)
        is_invoke = False

        if type == INVOKE_TX_TYPE:
            is_invoke = True

        if hash == b'\xa0ljY\xd8n\x1b\xb5\xdb\xa0\xf5d\xd8\xb3\xd8\xec\xf2\xfb\xe3E\xe3|3\xba\x83\xf2$jW\xa24':
            print("correct hash!")
        else:
            print("hash does not match")

    return ts
