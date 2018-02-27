from boa.interop.Neo.Runtime import Notify


def Main():

    m = [1, 2, 2]

    m.append(7)

    q = [6, 7]

    l = 'howdy'

    m.append(l)

    m.append(q)

    m.append(b'\x01')

    answer = q[0]

#    Notify(m)

    return m[5]
