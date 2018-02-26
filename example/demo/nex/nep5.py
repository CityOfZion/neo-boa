from boa.interop.Neo.Runtime import CheckWitness, Notify
from boa.interop.Neo.Action import RegisterAction
from boa.interop.Neo.Storage import *
from boa.builtins import concat

from example.demo.nex.token import *


OnTransfer = RegisterAction('transfer', 'addr_from', 'addr_to', 'amount')
OnApprove = RegisterAction('approve', 'addr_from', 'addr_to', 'amount')

NEP5_METHODS = ['name', 'symbol', 'decimals', 'totalSupply', 'balanceOf', 'transfer', 'transferFrom', 'approve', 'allowance']

ctx = GetContext()


def handle_nep51(operation, args):

    # these first 3 don't require get ctx

    if operation == 'name':
        return TOKEN_NAME

    elif operation == 'decimals':
        return TOKEN_DECIMALS

    elif operation == 'symbol':
        return TOKEN_SYMBOL

    arg_error = 'Incorrect Arg Length'

    if operation == 'totalSupply':
        return Get(ctx, TOKEN_CIRC_KEY)

    elif operation == 'balanceOf':
        if len(args) == 1:
            account = args[0]
            print("GETTING BALANCE")
            print(account)
            return Get(ctx, account)
        return arg_error

    elif operation == 'transfer':
        if len(args) == 3:
            t_from = args[0]
            t_to = args[1]
            t_amount = args[2]
            return do_transfer(t_from, t_to, t_amount)
        return arg_error

    elif operation == 'transferFrom':
        if len(args) == 3:
            t_from = args[0]
            t_to = args[1]
            t_amount = args[2]
            return do_transfer_from(t_from, t_to, t_amount)
        return arg_error

    elif operation == 'approve':
        if len(args) == 3:
            t_owner = args[0]
            t_spender = args[1]
            t_amount = args[2]
            return do_approve(t_owner, t_spender, t_amount)
        return arg_error

    elif operation == 'allowance':
        if len(args) == 2:
            t_owner = args[0]
            t_spender = args[1]
            return do_allowance(t_owner, t_spender)

        return arg_error

    return False


def do_transfer(t_from, t_to, amount):

    if amount <= 0:
        return False

    if len(t_to) != 20:
        return False

    if CheckWitness(t_from):

        if t_from == t_to:
            print("transfer to self!")
            return True

        from_val = Get(ctx, t_from)

        if from_val < amount:
            print("insufficient funds")
            return False

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
    else:
        print("from address is not the tx sender")

    return False


def do_transfer_from(t_from, t_to, amount):

    if amount <= 0:
        return False

    available_key = concat(t_from, t_to)

    if len(available_key) != 40:
        return False

    available_to_to_addr = Get(ctx, available_key)

    if available_to_to_addr < amount:
        print("Insufficient funds approved")
        return False

    from_balance = Get(ctx, t_from)

    if from_balance < amount:
        print("Insufficient tokens in from balance")
        return False

    to_balance = Get(ctx, t_to)

    new_from_balance = from_balance - amount

    new_to_balance = to_balance + amount

    Put(ctx, t_to, new_to_balance)
    Put(ctx, t_from, new_from_balance)

    print("transfer complete")

    new_allowance = available_to_to_addr - amount

    if new_allowance == 0:
        print("removing all balance")
        Delete(ctx, available_key)
    else:
        print("updating allowance to new allowance")
        Put(ctx, available_key, new_allowance)

    OnTransfer(t_from, t_to, amount)

    return True


def do_approve(t_owner, t_spender, amount):

    if not CheckWitness(t_owner):
        print("Incorrect permission")
        return False

    if amount < 0:
        print("Negative amount")
        return False

    from_balance = Get(ctx, t_owner)

    # cannot approve an amount that is
    # currently greater than the from balance
    if from_balance >= amount:

        approval_key = concat(t_owner, t_spender)

        if amount == 0:
            Delete(ctx, approval_key)
        else:
            Put(ctx, approval_key, amount)

        OnApprove(t_owner, t_spender, amount)

        return True

    return False


def do_allowance(t_owner, t_spender):

    allowance_key = concat(t_owner, t_spender)

    amount = Get(ctx, allowance_key)

    return amount
