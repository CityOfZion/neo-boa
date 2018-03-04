# tested


def Main(operation, a, b):

    if operation == '&':
        return a & b

    elif operation == '|':
        return a | b

    elif operation == '^':
        return a ^ b

    elif operation == '>>':
        return a >> b

    elif operation == '<<':
        return a << b

    elif operation == '%':
        return a % b

    elif operation == '//':
        return a // b

    elif operation == '/':
        return a / b

    elif operation == '~':
        return ~a

    return 'unknown'
