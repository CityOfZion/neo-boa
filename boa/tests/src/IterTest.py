from boa.code.builtins import range


def Main():
    """

    :return:
    """
    count = 0

    r = range(0, 4)

    for i in range(0, 4):
        count += wah(i, count)
#        h = wah()
#        print(count)

    return count


def wah(i, count):

    return count + 1 * i
