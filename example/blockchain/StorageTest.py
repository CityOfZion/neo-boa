from boa.interop.Neo.Storage import Get, Put, Delete, GetContext
from boa.interop.Neo.Runtime import Notify

context = GetContext()


def Main(operation, arg, val):

    print("context")

    if operation == 'sget':

        return Get(context, arg)

    elif operation == 'sput':

        Put(context, arg, val)
        return True

    elif operation == 'sdel':

        Delete(context, arg)
        return True

    return 'unknown operation'
