from boa.blockchain.vm.Neo.Runtime import Notify
from .stuff.storage_api import StorageAPI


def Main(a):

    storage = StorageAPI()

    storage.putitem('hello', 9)

    helloval = storage.getitem('hello')

    Notify(helloval)

    storage.deleteitem('hello')

    hval2 = storage.getitem('hello')

    Notify(hval2)

    # put it again
    storage.putitem('hello', 6)

    m = storage.getitem('hello')

    storage.putitem('h1', 2)
    storage.putitem('h2', 5)

    # this messes up the stack
    # res = storage.getitem('h1') + storage.getitem('h2')

    h1 = storage.getitem('h1')

    # this is ok?
    res = h1 + storage.getitem('h2')

    return res
