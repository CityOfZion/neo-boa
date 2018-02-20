#from boa.builtins import range


def Main():
    """

    :return:
    """
    items = [0, 1, 2]


    count = 0

    for i in items:

        count += i

        if i == 1:
            print("ONE!")
        else:
            print("NOT ONE!")


    return count
