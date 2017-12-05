from boa.blockchain.vm.Neo.App import DynamicAppCall
from boa.blockchain.vm.Neo.Runtime import Notify


def Main(a):

    print("will add")

#    Notify(a)

    m = b'd724c4191f83cee8d3c84e5d5bd91a054a9867d0'
    res = DynamicAppCall(m, a, a)

    Notify(res)
#    result = DynamicAppCall(b'\xd0g\x98J\x05\x1a\xd9[]N\xc8\xd3\xe8\xce\x83\x1f\x19\xc4$\xd7', 10, a)


#    print("did dynamic call!")

#    Notify(result)

    output = res + 28

#    print("will return output?")
    return output
