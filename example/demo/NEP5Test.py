"""
NEP5 Token
===================================

This file, when compiled to .avm format, would comply with the current NEP5 token standard on the NEO blockchain

Token standard is available in proposal form here:
`NEP5 Token Standard Proposal <https://github.com/neo-project/proposals/blob/master/nep-5.mediawiki>`_

Compilation can be achieved as such

>>> from boa.compiler import Compiler
>>> Compiler.load_and_save('./boa/tests/src/NEP5Test.py')


Below is the current implementation in Python


"""

from boa.interop.Neo.Runtime import Log, Notify
from boa.interop.System.ExecutionEngine import GetScriptContainer, GetExecutingScriptHash
from boa.interop.Neo.Transaction import *
from boa.interop.Neo.Blockchain import GetHeight, GetHeader
from boa.interop.Neo.Action import RegisterAction
from boa.interop.Neo.Runtime import GetTrigger, CheckWitness
from boa.interop.Neo.TriggerType import Application, Verification
from boa.interop.Neo.Output import GetScriptHash, GetValue, GetAssetId
from boa.interop.Neo.Storage import GetContext, Get, Put, Delete
from boa.interop.Neo.Header import GetTimestamp, GetNextConsensus

# -------------------------------------------
# TOKEN SETTINGS
# -------------------------------------------

TOKEN_NAME = 'LOCALTOKEN'
SYMBOL = 'LWTF'

OWNER = b'F\xc2\xbb\x9c\x17Ci\x89\xca\xa7\x85>|\xbd\x87B>H#\xf2'

DECIMALS = 8

FACTOR = 100000000


# -------------------------------------------
# ICO SETTINGS
# -------------------------------------------

NEO_ASSET_ID = b'\x9b|\xff\xda\xa6t\xbe\xae\x0f\x93\x0e\xbe`\x85\xaf\x90\x93\xe5\xfeV\xb3J\\"\x0c\xcd\xcfn\xfc3o\xc5'

# 5million times decimals ( factor )
TOTAL_AMOUNT = 500000000000000

PRE_ICO_CAP = 1000000000  # amount for the owner to start with

ICO_START_TIME = 1502726400  # August 14 2017
ICO_END_TIME = 1513936000  # December 22 2017

# -------------------------------------------
# Events
# -------------------------------------------

OnTransfer = RegisterAction('transfer', 'from', 'to', 'amount')

OnRefund = RegisterAction('refund', 'to', 'amount')


def Main(operation, args):
    """
    This is the main entry point for the Smart Contract

    :param operation: the operation to be performed ( eg `mintTokens`, `transfer`, etc)
    :type operation: str

    :param args: an optional list of arguments
    :type args: list

    :return: indicating the successful execution of the smart contract
    :rtype: bool
    """

    trigger = GetTrigger()

    if trigger == Verification():

        print("doing verification!")
        owner_len = len(OWNER)

        if owner_len == 20:

            res = CheckWitness(OWNER)
            print("owner verify result")
            return res

#        elif owner_len == 33:
#            #res = verify_signature(operation, OWNER)
#            Log("verify signature not understood by me yet")

    elif trigger == Application():

        print("doing application!")

        if operation == 'deploy':
            out = Deploy()
            print("deployed!")
            return out
        elif operation == 'mintTokens':
            domint = MintTokens()
            print("minted token!")
            return domint
        elif operation == 'totalSupply':
            supply = TotalSupply()
            print("got total supply")
            Notify(supply)
            return supply
        elif operation == 'name':
            n = Name()
            return n
        elif operation == 'decimals':
            d = Decimals()
            return d
        elif operation == 'symbol':
            sym = Symbol()
            return sym

        elif operation == 'transfer':
            print("do transfers")
            if len(args) == 3:
                t_from = args[0]
                t_to = args[1]
                t_amount = args[2]
                return DoTransfer(t_from, t_to, t_amount)

            else:
                return False

        elif operation == 'balanceOf':
            if len(args) == 1:

                print("do balance")

                account = args[0]

                balance = BalanceOf(account)
                print("got balance")
                Notify(balance)

                return balance

            else:

                return 0

    return False


def Name():
    """
    Method that returns the name of this NEP5 token

    :return: name of the token
    :rtype: str

    """
    print("getting name!")
    return TOKEN_NAME


def Symbol():
    """
    Method that returns the symbol of this NEP5 token

    :return: symbol of the token
    :rtype: str

    """
    print("getting symbol!")
    return SYMBOL


def Decimals():
    """
    Method that returns the number of decimals an NEP5 token uses

    :return: the number of decimals this NEP5 token uses
    :rtype: int

    """
    print("getting decimals...")
    return DECIMALS


def Deploy():
    """
    Method for the NEP5 Token owner to use in order to deploy an initial amount of tokens to their own address

    :return: whether the deploy was successful
    :rtype: bool
    """
    print("deploying!")

    isowner = CheckWitness(OWNER)

    if isowner:

        print("ok to deploy")
        context = GetContext()

        total = Get(context, 'totalSupply')

        if len(total) == 0:

            Log("WILL DEPLOY!")

            Put(context, OWNER, PRE_ICO_CAP)

            Put(context, "totalSupply", PRE_ICO_CAP)

            OnTransfer(0, OWNER, PRE_ICO_CAP)

            return True
        else:
            print("ALREADY DEPLOYED, wont do it again")

    print("only owner can deploy")
    return False


def MintTokens():
    """
    Method for an address to call in order to deposit NEO into the NEP5 token owner's address in exchange for a calculated amount of NEP5 tokens

    :return: whether the token minting was successful
    :rtype: bool

    """
    print("minting tokens!")

    tx = GetScriptContainer()

    references = tx.References

    print("helol1")
    if len(references) < 1:
        print("no neo attached")
        return False

    print("hello2")
    reference = references[0]
    print("hello2")
#    sender = reference.ScriptHash

    sender = GetScriptHash(reference)
    print("hello4")

    value = 0
    print("hello5")
    output_asset_id = GetAssetId(reference)
    if output_asset_id == NEO_ASSET_ID:

        print("hello6")
        receiver = GetExecutingScriptHash()
        print("hello7")
        for output in tx.Outputs:
            shash = GetScriptHash(output)
            print("getting shash..")
            if shash == receiver:
                print("adding value?")
                output_val = GetValue(output)
                value = value + output_val

        print("getting rate")
        rate = CurrentSwapRate()
        print("got rate")
        if rate == 0:
            OnRefund(sender, value)
            return False

        num_tokens = value * rate / 100000000

        context = GetContext()

        balance = Get(context, sender)

        new_total = num_tokens + balance

        Put(context, sender, new_total)

        total_supply = Get(context, 'totalSupply')

        new_total_supply = total_supply + num_tokens

        Put(context, 'totalSupply', new_total_supply)

        OnTransfer(0, sender, num_tokens)

        return True

    return False


def TotalSupply():
    """
    Method to return the total amount of NEP5 tokens in current circluation

    :return: the total number of tokens in circulation
    :rtype: int

    """
    print("total supply!")

    context = GetContext()

    res = Get(context, "totalSupply")

    print("got total supply")
    Notify(res)

    return res


def DoTransfer(t_from, t_to, amount):
    """
    Method to transfer NEP5 tokens of a specified amount from one account to another

    :param t_from: the address to transfer from
    :type t_from: bytearray

    :param t_to: the address to transfer to
    :type t_to: bytearray

    :param amount: the amount of NEP5 tokens to transfer
    :type amount: int

    :return: whether the transfer was successful
    :rtype: bool

    """
    if amount <= 0:
        print("cannot transfer zero or less")
        return False

    from_is_sender = CheckWitness(t_from)

    if from_is_sender:

        if t_from == t_to:
            return True

        context = GetContext()

        from_val = Get(context, t_from)

        if from_val < amount:
            print("Insufficient funds")
            return False

        if from_val == amount:
            print("Removing all funds!")
            Delete(context, t_from)

        else:
            difference = from_val - amount
            Put(context, t_from, difference)

        to_value = Get(context, t_to)

        to_total = to_value + amount

        Put(context, t_to, to_total)

        OnTransfer(t_from, t_to, amount)

        return True
    else:
        print("from address is not the tx sender")

    return False


def BalanceOf(account):
    """
    Method to return the current balance of an address

    :param account: the account address to retrieve the balance for
    :type account: bytearray

    :return: the current balance of an address
    :rtype: int

    """
    print("getting balance of...")
    context = GetContext()
    print("getting context...")
    balance = Get(context, account)
    print("got balance...")

    return balance


def CurrentSwapRate():
    """
    Method to calculate the current 'going rate' or exchange ratio of NEO to NEP5 tokens

    :return: the current rate
    :rtype: int

    """
    basic = 1000 * FACTOR
    duration = ICO_END_TIME - ICO_START_TIME
    print("getting swap rate")
    context = GetContext()
    print("got context")

    total_supply = Get(context, 'totalSupply')
    print("got total supply")
    if total_supply >= TOTAL_AMOUNT:
        return False
    print("getting current height...")
    currentHeight = GetHeight()
    print("got current height")
    currentBlock = GetHeader(currentHeight)
    print("got current block...")
    time = currentBlock.Timestamp - ICO_START_TIME

    if time < 0:

        return 0

    elif time < 86400:
        return basic * 130 / 100

    elif time < 259200:
        return basic * 120 / 100

    elif time < 604800:
        return basic * 110 / 100

    elif time < duration:
        return basic

    return 0
