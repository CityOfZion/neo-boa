"""
Large Array Storage Test

A simple utilise contract that allows you to manipulate a stored list for stress tests and GAS cost evaluation.

Test Command:
    build [FILE_PATH] test 0710 05 True False init

Example Executions:
    testinvoke [CONTRACT_HASH] init
    testinvoke [CONTRACT_HASH] delete
    testinvoke [CONTRACT_HASH] fetch
    testinvoke [CONTRACT_HASH] count
    testinvoke [CONTRACT_HASH] append_1
    testinvoke [CONTRACT_HASH] append_10
"""
from boa.interop.Neo.Storage import Get, Put, Delete, GetContext
from boa.interop.Neo.Runtime import Log, Notify
from boa.builtins import concat, list, range, take, substr

# -- Global variables
KEY = 'test_array'


def Main(operation, args):
    """

    :param operation: The name of the operation to perform
    :param args: A list of arguments along with the operation
    :type operation: str
    :type args: list
    :return: The result of the operation
    :rtype: bytearray
    """
    if operation == 'init':
        return do_init()
    elif operation == 'delete':
        return do_delete()
    elif operation == 'fetch':
        return do_fetch()
    elif operation == 'count':
        return do_count()
    elif operation == 'append_1':
        return do_append_1()
    elif operation == 'append_10':
        return do_append_10()
    else:
        Notify('unknown operation')
        return False


def do_init():
    """
    Initialize the storage by setting an empty list.

    :return: indication success execution of the command
    :rtype: bool
    """
    context = GetContext()
    init_list_bytes = serialize_array([])
    Put(context, KEY, init_list_bytes)
    return True


def do_delete():
    """
    Delete the storage and reset back to its default state.

    :return: indication success execution of the command
    :rtype: bool
    """
    context = GetContext()
    Delete(context, KEY)
    return True


def do_fetch():
    """
    Fetch current list value from storage.

    :return: the stored list value
    :rtype: list
    """
    context = GetContext()
    list_bytes = Get(context, KEY)
    return deserialize_bytearray(list_bytes)


def do_count():
    """
    Fetch length of the stored list.

    :return: the stored list value
    :rtype: int
    """
    context = GetContext()
    list_bytes = Get(context, KEY)
    item_list = deserialize_bytearray(list_bytes)
    return len(item_list)


def do_append_1():
    """
    Add 1 item into the list in storage.

    :return: indication success execution of the command
    :rtype: bool
    """
    context = GetContext()
    list_bytes = Get(context, KEY)
    item_list = deserialize_bytearray(list_bytes)
    item_list.append('single item')
    list_length = len(item_list)
    Log('new list length:')
    Log(list_length)
    list_bytes = serialize_array(item_list)
    Put(context, KEY, list_bytes)
    return True


def do_append_10():
    """
    Add 10 items into the list in storage.

    :return: indication success execution of the command
    :rtype: bool
    """
    context = GetContext()
    list_bytes = Get(context, KEY)
    item_list = deserialize_bytearray(list_bytes)
    addition_list = [
        '1 of 10', '1 of 10', '1 of 10', '1 of 10', '1 of 10', '1 of 10', '1 of 10', '1 of 10', '1 of 10', '1 of 10'
    ]
    for item in addition_list:
        item_list.append(item)
    list_length = len(item_list)
    Log('new list length:')
    Log(list_length)
    list_bytes = serialize_array(item_list)
    Put(context, KEY, list_bytes)
    return True


def deserialize_bytearray(data):

    # get length of length
    collection_length_length = data[0:1]

    # get length of collection
    collection_len = data[1:collection_length_length + 1]

    # create a new collection
    new_collection = list(length=collection_len)

    # trim the length data
    offset = 1 + collection_length_length

    for i in range(0, collection_len):

        # get the data length length
        itemlen_len = data[offset:offset + 1]

        # get the length of the data
        item_len = data[offset + 1:offset + 1 + itemlen_len]

        # get the data
        item = data[offset + 1 + itemlen_len: offset + 1 + itemlen_len + item_len]

        # store it in collection
        new_collection[i] = item

        offset = offset + item_len + itemlen_len + 1

    return new_collection


def serialize_array(items):

    # serialize the length of the list
    itemlength = serialize_var_length_item(items)

    output = itemlength

    # now go through and append all your stuff
    for item in items:

        # get the variable length of the item
        # to be serialized
        itemlen = serialize_var_length_item(item)

        # add that indicator
        output = concat(output, itemlen)

        # now add the item
        output = concat(output, item)

    # return the stuff
    return output


def serialize_var_length_item(item):

    # get the length of your stuff
    stuff_len = len(item)

    # now we need to know how many bytes the length of the array
    # will take to store

    # this is one byte
    if stuff_len <= 255:
        byte_len = b'\x01'
    # two byte
    elif stuff_len <= 65535:
        byte_len = b'\x02'
    # hopefully 4 byte
    else:
        byte_len = b'\x04'

    out = concat(byte_len, stuff_len)

    return out
