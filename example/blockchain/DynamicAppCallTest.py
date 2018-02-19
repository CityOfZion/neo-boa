from boa.interop.Neo.App import DynamicAppCall
from boa.interop.Neo.Runtime import Notify

# Note this is a new api, not ready for mainnet yet


def Main(a):

    print("will add")

#    m = b'd724c4191f83cee8d3c84e5d5bd91a054a9867d0'
    m = b'\xd0g\x98J\x05\x1a\xd9[]N\xc8\xd3\xe8\xce\x83\x1f\x19\xc4$\xd7'
    res = DynamicAppCall(m, a, a)

    Notify(res)

    output = res + 28

#    print("will return output?")
    return output
