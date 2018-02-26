# tested

from boa.interop.Neo.Blockchain import GetTransaction
from boa.interop.Neo.Transaction import *
from boa.interop.Neo.Output import *
from boa.interop.Neo.Input import GetInputHash, GetIndex

NEO = b'\x9b|\xff\xda\xa6t\xbe\xae\x0f\x93\x0e\xbe`\x85\xaf\x90\x93\xe5\xfeV\xb3J\\"\x0c\xcd\xcfn\xfc3o\xc5'
GAS = b'\xe7-(iy\xeel\xb1\xb7\xe6]\xfd\xdf\xb2\xe3\x84\x10\x0b\x8d\x14\x8ewX\xdeB\xe4\x16\x8bqy,`'


def Main(operation, txid):

    tx = GetTransaction(txid)

    if not tx:
        return False

    if operation == 'get_hash':
        return tx.Hash

    elif operation == 'get_type':
        return tx.Type

    elif operation == 'get_attrs':
        return tx.Attributes

    elif operation == 'get_inputs':
        return tx.Inputs

    elif operation == 'get_outputs':
        return tx.Outputs

    elif operation == 'get_references':
        return tx.References

    elif operation == 'get_unspent':
        return tx.UnspentCoins

    elif operation == 'get_output_details':
        res = []

        for item in tx.Outputs:
            subres = []
            subres.append(item.Value)
            subres.append(item.AssetId)
            subres.append(item.ScriptHash)
            res.append(subres)

        return res

    elif operation == 'get_reference_details':
        res = []
        refs = tx.References

        for item in refs:
            subres = []
            subres.append(item.Value)
            subres.append(item.AssetId)
            subres.append(item.ScriptHash)
            res.append(subres)

        return res

    # @TODO
    # For some reason, if theres a bunch of iterations
    # in a row, then the last one fails?
#    elif operation == 'get_unspent_details':
#        res2 = []
#        uns = tx.UnspentCoins
#        for item2 in uns:
#            subres = []
#            subres.append(item2.Value)
#            subres.append(item2.AssetId)
#            subres.append(item2.ScriptHash)
#            res2.append(subres)
#
#        return res2

        # @TODO
    # name clash with Input.GetHash and Transaction.GetHash
    elif operation == 'get_input_details':
        res = []
        inputs = tx.Inputs
        input1 = inputs[0]
        inputhash = GetInputHash(input1)
        inputIndex = input1.Index

        return [inputhash, inputIndex]

    return 'unknown operation'
