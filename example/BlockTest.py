from boa.interop.Neo.Blockchain import GetBlock
from boa.interop.Neo.Runtime import Notify, Log


def Main():
    """

    :return:
    """
    block_height = 123234
    block = GetBlock(block_height)

    print("hello")
    Notify(block)

    a = 1

    return block_height
