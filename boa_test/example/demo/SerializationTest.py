from boa.interop.Neo.Runtime import Notify, Serialize, Deserialize
from boa.interop.Neo.Storage import Put, Get, GetContext

ctx = GetContext()


def Main(operation):

    # create an array
    stuff = ['a', 3, ['j', 3, 5], 'jk', 'lmnopqr']

    # serialize it
    to_save = Serialize(stuff)
    Put(ctx, 'serialized', to_save)

    if operation == 1:
        return to_save

    elif operation == 2:

        to_retrieve = Get(ctx, 'serialized')
        return to_retrieve

    elif operation == 3:

        to_retrieve = Get(ctx, 'serialized')
        deserialized = Deserialize(to_retrieve)
        return deserialized

    elif operation == 4:

        to_retrieve = Get(ctx, 'serialized')
        deserialized = Deserialize(to_retrieve)
        return deserialized[2]

    return False
