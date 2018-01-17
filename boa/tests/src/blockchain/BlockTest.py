from boa.blockchain.vm.Neo.Blockchain import GetBlock
from boa.blockchain.vm.Neo.Runtime import Notify
from boa.blockchain.vm.Neo.Block import GetTransactions


def Main():

    #    blockhash = b'\xe9F.\xbd\x83\x99\xb4\xa3Z\xdc\xdde\xe5^\xed\xf6\x9f\x82\xa3\x14\xc9y\x04\xb8\xfe\x8cb\xafO.\xe7\xd9'
    """

    :return:
    """
    block_height = 1234
    block = GetBlock(block_height)

    print("hello")
    Notify(block)

    h = block.Transactions

    Notify(h)

    return 4
