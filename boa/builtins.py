

class list(list):

    """
    list() -> new empty list
    list(length=x) -> new list initialized with length of x
    """

#    def __init__(self, length=0):
#        pass
    pass


def concat(str1, str2):
    """
     range(str1, str2) -> str object

     Return a string that is the concatenation of the two arguments ( str1 + str2 )
     """
    pass


def keys(dictionary):
    """
     k = keys(mydict)

     pushes a list of a dictionary keys onto the stack
     """
    pass


def values(dictionary):
    """
     v = values(mydict)

     pushes a list of a dictionary values onto the stack
     """
    pass


def has_key(dictionary, key):
    """
     val = has_key(mydict, 'b')

     pushes a boolean of wether a dictionary has a key onto the stack
     """
    pass


# This is not necessary.  you can use mystring[start:end]
# Actually, it is currently necessary, as mystring[start:end] is not working as expected

def substr(source, start_index, count):
    """
    substr(source, start_index, count) -> list object

    Return a subset of a string `source`, starting at `start_index` and
    of length `count`
    """
    pass


def take(source, count):
    """
    take(source, count) -> list object

    Return a subset of a string or list `source`, starting
    at index 0 and of length `count`
    """
    pass


def range(start, stop):
    """
    range(start, stop) -> list object

    Return an list that is a a sequence of integers from start (inclusive)
    to stop (exclusive).  range(i, j) produces i, i+1, i+2, ..., j-1.
    """

    length = stop - start

    out = list(length=length)

    index = 0

    orig_start = start

    while start < stop:
        val = index + orig_start
        out[index] = val
        index = index + 1
        start = orig_start + index

    return out


def sha1(data):
    """

    :param data:
    """
    pass


def sha256(data):
    """

    :param data:
    """
    pass


def hash160(data):
    """

    :param data:
    """
    pass


def hash256(data):
    """

    :param data:
    """
    pass


def verify_signature(pubkey, signature, message):
    """
    :param pubkey:
    :param signature:
    :param message:
    """
    pass


def throw_if_null(item):
    pass


def breakpoint():
    """
    Adds a breakpoint to the debug map
    """
    pass
