# tested

from boa.builtins import concat
from boa.interop.Neo.Runtime import Notify


def Main():

    items = [0, 1, 2]

    items2 = ['a', 'b', 'c', 'd']
    count = 0

    for i in items:  # 3

        count += 1

        for j in items2:  # 4

            count += 1

            for k in items:  # 3
                count += 1

    return count
