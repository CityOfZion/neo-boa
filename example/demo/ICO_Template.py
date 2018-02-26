"""
NEX ICO Template
===================================

Author: Thomas Saunders
Email: tom@neonexchange.org

Date: Dec 11 2017

"""

from boa.interop.Neo.Runtime import GetTrigger, CheckWitness, Notify
from boa.interop.Neo.TriggerType import Application, Verification
from boa.interop.Neo.Storage import *
from example.demo.nex.txio import get_asset_attachments
from example.demo.nex.token import *
from example.demo.nex.crowdsale import can_exchange, exchange, kyc_register, kyc_status
from example.demo.nex.nep5 import NEP5_METHODS, handle_nep51

ctx = GetContext()


def Main(operation, args):
    """

    :param operation: str The name of the operation to perform
    :param args: list A list of arguments along with the operation
    :return:
        bytearray: The result of the operation
    """

    trigger = GetTrigger()

    # This is used in the Verification portion of the contract
    # To determine whether a transfer of system assets ( NEO/Gas) involving
    # This contract's address can proceed
    if trigger == Verification():

        # check if the invoker is the owner of this contract
        is_owner = CheckWitness(TOKEN_OWNER)

        # If owner, proceed
        if is_owner:

            return True

        # Otherwise, we need to lookup the assets and determine
        # If attachments of assets is ok
        attachments = get_asset_attachments()

        return can_exchange(attachments, True)

    elif trigger == Application():

        for op in NEP5_METHODS:
            if operation == op:
                return handle_nep51(operation, args)

        if operation == 'deploy':
            return deploy()

        if operation == 'circulation':
            return get_circulation()

        # the following are handled by crowdsale

        if operation == 'mintTokens':
            return exchange()

        if operation == 'crowdsale_register':
            return kyc_register(args)

        if operation == 'crowdsale_status':
            return kyc_status(args)

        if operation == 'crowdsale_available':
            return crowdsale_available_amount()

        return 'unknown operation'

    return False


def deploy():
    """

    :param token: Token The token to deploy
    :return:
        bool: Whether the operation was successful
    """
    if not CheckWitness(TOKEN_OWNER):
        print("Must be owner to deploy")
        return False

    if not Get(ctx, 'initialized'):
        # do deploy logic
        Put(ctx, 'initialized', 1)
        Put(ctx, TOKEN_OWNER, TOKEN_INITIAL_AMOUNT)
        return add_to_circulation(TOKEN_INITIAL_AMOUNT)

    return False
