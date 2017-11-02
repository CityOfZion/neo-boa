
def Main():

    print('hello!')

    a = b'\x03'

    b = 3

    if a == b:

        print("equal!!")

    else:

        print("not equal!")

    if sample_method_call() == sample_method_call_2():
        print("method equal")
    else:
        print("method not equal")

    if a is b:

        print("is!")

    else:

        print("not is!")

    return True


def sample_method_call():

    return 2


def sample_method_call_2():

    return 2
