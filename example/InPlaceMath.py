# tested

def Main():
    """

    :return:
    """
    a = 1

    c = 3

    a += c # 4

    b = 10

    b -= a # 6

    d = 2

    b *= d # 12

    b /= c # 4

    b %= 3 # 1

    f = b + 20 # 21

#    f |= 34 # this doesn't curretly work

    return f  # expect 21
