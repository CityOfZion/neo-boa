from boa.interop.Neo.Runtime import Notify
from boa.interop.Neo.Storage import Get, GetContext, Put
from boa.builtins import concat, list, range, take, substr


# this is the same thing as SerializationTest1, but using slice notation instead of substr

SERIALIZED_NAME = 'AWESOME'


def Main():

    # create an array
    stuff = ['a', 'def', 'ghi', 'jk', 'lmnopqr']

    # serialize it
    to_save = serialize_array(stuff)

    # now lets store it
    context = GetContext()
    Put(context, SERIALIZED_NAME, to_save)

    # now retrieve it from storage
    serialized = Get(context, SERIALIZED_NAME)

    # now rebuild the array
    re_constructed = deserialize_bytearray(serialized)

    # iterate over the array to show its items match ``stuff``
    for item in re_constructed:
        Notify(item)

    # return the reconstructed array
    return re_constructed


def deserialize_bytearray(data):

    # ok this is weird.  if you remove this print statement, it stops working :/

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
