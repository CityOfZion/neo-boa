from boa.interop.Neo.App import DynamicAppCall
from boa.interop.Neo.Runtime import Notify

# Note this is a new api, not ready for mainnet yet


def Main(hash, operation, a, b):

    res = DynamicAppCall(hash, operation, a, b)

    return res
