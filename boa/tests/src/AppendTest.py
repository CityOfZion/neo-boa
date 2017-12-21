from boa.blockchain.vm.Neo.Runtime import Notify


def Main():
    """

    :return:
    """
    m = [1, 2, 4, 'blah']

    m.append(7)

    q = [6, 7]

    l = 'howdy'

    m.append(l)

    m.append(q)

    m.append(b'\x01')

#    answer = j[0]

    Notify(m)

    return m[5]
