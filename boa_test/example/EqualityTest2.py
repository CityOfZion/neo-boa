
def Main(operation):

    if operation == 1:
        a = 'deploy'

        b = bytearray(b'deploy\x00\x00')

        return a == b

    elif operation == 2:

        a = 'deploy'

        b = bytearray(b'deploy')

        return a == b

    elif operation == 3:

        a = b'deploy'
        b = 'deploy'
        return a == b

    elif operation == 4:

        a = 0
        b = False
        return a == b

    elif operation == 5:

        a = 0
        b = ''
        return a == b

    elif operation == 6:

        a = False
        b = ''
        return a == b

    elif operation == 7:

        a = False
        b = -1
        return a == b
