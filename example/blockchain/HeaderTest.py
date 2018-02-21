from boa.interop.Neo.Blockchain import GetHeader
from boa.interop.Neo.Header import GetMerkleRoot, GetTimestamp, GetHash, GetVersion, GetNextConsensus

from boa.interop.Neo.Runtime import Notify, Log


def Main(block_height):

    header = GetHeader(block_height)

    Log("got header")

    merkle = GetMerkleRoot(header)

    version = GetVersion(header)

    Notify(version)

    hash = GetHash(header)

    Notify(hash)

    print("got merkle")

    Notify(header)

    a = 1

    Notify(merkle)

    print("getting timestamp")
    ts = GetTimestamp(header)

    Notify(ts)

    if ts == 1494640540:

        return 9

    return a
