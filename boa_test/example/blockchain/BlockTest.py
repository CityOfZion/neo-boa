# tested

from boa.interop.Neo.Blockchain import GetBlock
from boa.interop.Neo.Block import *


def Main(operation, height):

    block = GetBlock(height)

    if operation == 'get_hash':
        return block.Hash

    elif operation == 'get_index':
        return block.Index

    elif operation == 'get_timestamp':
        return block.Timestamp

    elif operation == 'get_prevhash':
        return block.PrevHash

    elif operation == 'get_version':
        return block.Version

    elif operation == 'get_nextconsensus':
        return block.NextConsensus

    elif operation == 'get_merkleroot':
        return block.MerkleRoot

    elif operation == 'get_consensusdata':
        return block.ConsensusData

    elif operation == 'get_transactioncount':
        return block.TransactionCount

    elif operation == 'get_transactions':
        return block.Transactions

    elif operation == 'get_transaction':
        return GetTransaction(block, 0)

    return 'unknown operation'
