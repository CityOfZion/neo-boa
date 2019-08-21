"""
NEP5 Token
===================================


.. moduleauthor:: Thomas Saunders <tom@cityofzion.io>, Joe Stewart <joe@coz.io>

This file, when compiled to .avm format, would comply with the current NEP5 token standard on the NEO blockchain

Token standard is available in proposal form here:
`NEP5 Token Standard Proposal <https://github.com/neo-project/proposals/blob/master/nep-5.mediawiki>`_

Compilation can be achieved as such

>>> from boa.compiler import Compiler
>>> Compiler.load_and_save('./boa/tests/src/NEP5.py')

Or, from within the neo-python shell
``sc build_run path/to/NEP5.py True False True 0710 05 name []``


Below is the current implementation in Python


"""

from boa.interop.Neo.Runtime import GetTrigger, CheckWitness
from boa.interop.Neo.Action import RegisterAction
from boa.interop.Neo.TriggerType import Application, Verification
from boa.interop.Neo.Storage import GetContext, Get, Put, Delete
from boa.interop.System.ExecutionEngine import GetCallingScriptHash
from boa.interop.Neo.Blockchain import GetContract
from boa.builtins import concat

# -------------------------------------------
# TOKEN SETTINGS
# -------------------------------------------

OWNER = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
# Script hash of the contract owner

# Name of the Token
TOKEN_NAME = 'NEP5 Standard'

# Symbol of the Token
TOKEN_SYMBOL = 'NEP5'

# Number of decimal places
TOKEN_DECIMALS = 8

# Total Supply of tokens in the system
TOKEN_TOTAL_SUPPLY = 10000000 * 100000000  # 10m total supply * 10^8 ( decimals)

ctx = GetContext()

# -------------------------------------------
# Events
# -------------------------------------------

OnTransfer = RegisterAction('transfer', 'addr_from', 'addr_to', 'amount')
OnApprove = RegisterAction('approve', 'addr_from', 'addr_to', 'amount')
OnError = RegisterAction('error', 'message')


def Main(operation, args):
    """
    This is the main entry point for the Smart Contract

    :param operation: the operation to be performed ( eg `balanceOf`, `transfer`, etc)
    :type operation: str
    :param args: a list of arguments ( which may be empty, but not absent )
    :type args: list
    :return: indicating the successful execution of the smart contract
    :rtype: bool
    """

    # The trigger determines whether this smart contract is being
    # run in 'verification' mode or 'application'

    trigger = GetTrigger()

    # 'Verification' mode is used when trying to spend assets ( eg NEO, Gas)
    # on behalf of this contract's address
    if trigger == Verification():

        # if the script that sent this is the owner
        # we allow the spend
        assert CheckWitness(OWNER), 'unauthorized'
        return True 

    # 'Application' mode is the main body of the smart contract
    elif trigger == Application():

        if operation == 'name':
            return TOKEN_NAME

        elif operation == 'decimals':
            return TOKEN_DECIMALS

        elif operation == 'symbol':
            return TOKEN_SYMBOL

        elif operation == 'totalSupply':
            return TOKEN_TOTAL_SUPPLY

        elif operation == 'balanceOf':
            assert len(args) == 1, 'incorrect arg length'
            account = args[0]
            return do_balance_of(ctx, account)

        elif operation == 'transfer':
            assert len(args) == 3, 'incorrect arg length'
            t_from = args[0]
            t_to = args[1]
            t_amount = args[2]
            return do_transfer(ctx, t_from, t_to, t_amount, GetCallingScriptHash())

        AssertionError('unknown operation')


def do_balance_of(ctx, account):
    """
    Method to return the current balance of an address

    :param account: the account address to retrieve the balance for
    :type account: bytearray

    :return: the current balance of an address
    :rtype: int

    """

    assert len(account) == 20, "invalid address"
    return Get(ctx, account)


def do_transfer(ctx, t_from, t_to, amount, caller):
    """
    Method to transfer NEP5 tokens of a specified amount from one account to another

    :param t_from: the address to transfer from
    :type t_from: bytearray
    :param t_to: the address to transfer to
    :type t_to: bytearray
    :param amount: the amount of NEP5 tokens to transfer
    :type amount: int
    :param caller: the scripthash of the calling script
    :type caller: bytearray

    :return: whether the transfer was successful
    :rtype: bool

    """

    assert amount > 0, "invalid amount"
    assert len(t_from) == 20, "invalid from address"
    assert len(t_to) == 20, "invalid to address"
    assert CheckWitnessOrCaller(t_from, caller), "transfer not authorized"

    if t_from == t_to:
        print("transfer to self!")
        return True

    from_val = Get(ctx, t_from)
    assert from_val >= amount, "insufficient funds"

    if from_val == amount:
        Delete(ctx, t_from)

    else:
        difference = from_val - amount
        Put(ctx, t_from, difference)

    to_value = Get(ctx, t_to)

    to_total = to_value + amount

    Put(ctx, t_to, to_total)

    OnTransfer(t_from, t_to, amount)

    return True


def CheckWitnessOrCaller(scripthash, caller):
    """ 
    Method to check if the transaction is signed by a private key
    or is the scripthash of a contract that is authorized to perform
    the requested function for its own address only

    :param scripthash: the scripthash to be checked
    :type scripthash: bytearray
    :param caller: the scripthash of the calling script
    :type caller: bytearray

    :return: whether the scripthash is authorized
    :rtype: bool

    """

    if GetContract(scripthash):
        if scripthash == caller: 
            return True  # a contract can spend its own funds
        else:
            # deny third-party contracts from transferring
            # tokens of a user even with the user signature
            # (this will break ability of some DEX to list the token)
            return False

    return CheckWitness(scripthash)


def AssertionError(msg):
    """
    Method to throw an exception (required by assert)
    - will log a notification to the neo-cli ApplicationLog
    to aid in post-transaction troubleshooting and analysis

    :param msg: error message
    :type msg: string

    """

    OnError(msg)
    raise Exception(msg)
