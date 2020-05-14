from boa.abi import *


@abi_method(String, Array, Any)
def main(operation, args):
    if operation == 'add':
        a = args[0]
        b = args[1]
        return add(a, b)
    else:
        return False


def add(a, b):
    return a + b
