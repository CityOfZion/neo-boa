from boa.interop.Neo.Storage import Get, Put, Delete, Find, GetContext
from boa.interop.Neo.Iterator import IterNext, IterKey, IterValue
from boa.interop.Neo.Runtime import Notify

ctx = GetContext()


def Main(query):

    Put(ctx, 'prefix1euo', 1)
    Put(ctx, 'prefix1e', 2)
    Put(ctx, 'prefix1__osetuh', 3)

    Put(ctx, 'blah', 'Hello Storage Find')

    result_iter = Find(ctx, query)

    items = []
    keys = []
    count = 0
    while IterNext(result_iter):
        val = IterValue(result_iter)
        items.append(val)
        keys.append(IterKey(result_iter))
        if query == 'pre' and count == 1:
            break

        count += 1

    if query == 'pref':
        return keys

    return items
