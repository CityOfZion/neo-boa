# tested

from boa.interop.Neo.Blockchain import GetTransaction
from boa.interop.Neo.Transaction import *
from boa.interop.Neo.Output import *
from boa.interop.Neo.Input import GetInputHash, GetIndex
from boa.interop.Neo.Witness import *
from boa.builtins import hash160
from boa.interop.System.ExecutionEngine import GetScriptContainer

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

    elif operation == 'get_witnesses':
        res = []
        witnesses = tx.Witnesses
        for item in witnesses:
            witness = {
                'verification': item.VerificationScript
            }
            res.append(witness)
        return res

    elif operation == 'get_witness_scripthashes':
        tx = GetScriptContainer()
        witnesses = tx.Witnesses
        res = []
        for item in witnesses:
            verification = item.VerificationScript
            script_hash = hash160(verification)
            res.append(script_hash)
        return res

    # name clash with Input.GetHash and Transaction.GetHash
    elif operation == 'get_input_details':
        res = []
        inputs = tx.Inputs
        input1 = inputs[0]
        inputhash = GetInputHash(input1)
        inputIndex = input1.Index

        return [inputhash, inputIndex]

    return 'unknown operation'
