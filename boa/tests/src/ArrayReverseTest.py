from boa.blockchain.vm.Neo.Runtime import Notify


def Main():

    # lets have fun

    # this dosen't work. sad
    #        m = [[1,2,3],'fun','cool','neo']
    """

    :return:
    """
    m = [1, 2, 4, 'blah']

    m.reverse()

    Notify(m)

    m.reverse()

    return m[0]
