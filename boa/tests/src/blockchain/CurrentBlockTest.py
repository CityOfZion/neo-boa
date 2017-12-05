from boa.blockchain.vm.Neo.Runtime import Notify, Log,GetCurrentBlock
from boa.blockchain.vm.Neo.Block import *
from boa.blockchain.vm.Neo.Blockchain import GetHeader


def Main():

    #    blockhash = b'\xe9F.\xbd\x83\x99\xb4\xa3Z\xdc\xdde\xe5^\xed\xf6\x9f\x82\xa3\x14\xc9y\x04\xb8\xfe\x8cb\xafO.\xe7\xd9'
    """

    :return:
    """

    print("hello?")
    block = GetCurrentBlock()

    index = block.Index
    print("hello")


    hash = block.Hash


    header = GetHeader(index)

    Notify(hash)

    Notify(header)

    Notify(header.Index)

    return index
