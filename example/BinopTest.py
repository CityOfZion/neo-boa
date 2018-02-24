# tested


def Main(operation, a, b):

    if operation == '&':
        print("DOING AND!")
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
