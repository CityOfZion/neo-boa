

from boa.interop.Neo.Blockchain import GetHeader
from boa.interop.Neo.Runtime import Notify
from boa.interop.Neo.Storage import GetContext, Get

from boa.builtins import concat


def Main(a, b):

    c = a + b

    header = GetHeader(345)

    header2 = GetHeader(2321)

    # this does not work
#    header3 = GetHeader( get_block_height())

    # this does work?
    header3 = GetHeader(get_block_height)

    # this does not work
#    header4 = GetHeader( get_block_height_again(4) )

    # test wether you can pass an object property to method calls
    res = process_hash(header.Hash, header2.Hash)
    # expect bytearray(b'\x86\xdce\x18\x13\x90\x8d\x9f\x8bsi\x87l\x06x\xd6\xc6g\x13\xc7E\x83\xc9\xf4>P\xbc\x18\xfd\xcd\xec\xc7\xa3\xd5B\xe6{G\x84d\xa5\xc3!\xc5_\xe3\x8aE*C\x98r\xd7k\x8f3Q6y\xf3\x95\xc5\xc1;')

    # test compairing object properties
    if header2.Timestamp > header.Timestamp:
        print("header 2 is less")
    else:
        print("header 1 is less")

    # this messes things up
    # method_without_return()

    # this is ok, even if method doesnt return anything
#    n = method_without_return()

    # this also works
    n = method_without_return

    # test returning the results of object properties
    return header.Timestamp + header2.Timestamp


def process_hash(h1, h2):

    return concat(h1, h2)


def process_other(a1, a2):

    return concat(a1, a2)


def method_without_return():

    m = 43

    q = 3


def get_block_height():

    return 83


def get_block_height_again(a):

    return a * 2
