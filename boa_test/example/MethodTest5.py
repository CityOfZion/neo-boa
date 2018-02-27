# tested


def Main():

    mylist = [1, 4, 6, 9, 13]

    d2 = add(mylist[0], mylist[2], get_a_value(mylist[1]))

    return d2


def add(a, b, c):

    result = a + b + c

    return result


def get_a_value(m):

    return m + 4
