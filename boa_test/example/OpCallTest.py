# tested

from boa.builtins import sha1, sha256, hash160, hash256


def Main(operation, a, b):

    if operation == 'omin':
        return min(a, b)

    elif operation == 'omax':
        return max(a, b)

    elif operation == 'oabs':
        return abs(a)

    elif operation == 'sha1':
        return sha1(a)

    elif operation == 'sha256':
        return sha256(a)

    elif operation == 'hash160':
        return hash160(a)

    elif operation == 'hash256':
        return hash256(a)

    return 'unknown'
