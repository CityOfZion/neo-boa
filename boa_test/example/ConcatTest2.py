# tested

from boa.builtins import concat


def Main(operation, args):
    if operation == 'concat':
        return do_concat(args)
    else:
        return False


def do_concat(args):
    if len(args) > 1:
        a = args[0]
        b = args[1]
        output = concat(a, b)
        return output
    return False
