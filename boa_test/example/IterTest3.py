# tested


def Main():

    items = [0, 1, 2]

    count = 0

    for i in items:

        count += i

        if i == 1:
            print("ONE!")

            count += what()

        else:
            count -= minus(i)

    return count


def what():

    return 8


def minus(a):
    return a + 1
