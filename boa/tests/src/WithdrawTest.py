from boa.blockchain.vm.Neo.Runtime import Notify, GetTrigger, CheckWitness
from boa.blockchain.vm.Neo.Action import RegisterAction
from boa.blockchain.vm.Neo.TriggerType import Application, Verification

from boa.blockchain.vm.Neo.TransactionType import InvocationTransaction
from boa.blockchain.vm.Neo.Transaction import *

from boa.blockchain.vm.System.ExecutionEngine import GetScriptContainer, GetExecutingScriptHash
from boa.blockchain.vm.Neo.TriggerType import Application, Verification
from boa.blockchain.vm.Neo.Output import GetScriptHash, GetValue, GetAssetId
from boa.blockchain.vm.Neo.Storage import GetContext, Get, Put, Delete

OWNER = b'\x13\xff4\xcc\x10\x1cVs\x7fe\xc3\xb3\xd2\xf9iTHESK'

NEO_ASSET_ID = b'\x9b|\xff\xda\xa6t\xbe\xae\x0f\x93\x0e\xbe`\x85\xaf\x90\x93\xe5\xfeV\xb3J\\"\x0c\xcd\xcfn\xfc3o\xc5'


onDeposit = RegisterAction('deposit', 'account', 'amount')
onWithdraw = RegisterAction('withdraw', 'account', 'amount')
onWithdrawReconciled = RegisterAction('withdraw_reconcile', 'account', 'amount')


def Main(args):

    print("Do Withdraw Test")

    trigger = GetTrigger()

    if trigger == Verification():

        print("doing verification")

        # check to see if the withdrawer is the owner

        is_owner = CheckWitness(OWNER)

        # always allow owner to withdraw
        if is_owner:
            return True

        else:

            # if it is not the owner, we need to verify a few things
            print("will test can withdraw")
            can_widthraw = CanWithdrawNeo()

            print("can withdraw neo?")
#            Notify(can_widthraw)

            return can_widthraw

    elif trigger == Application():
        print("doing application")

        # no matter what happens, we need to reconcile balances
        # so if, for example, someone has sucessfully made a withdrawl
        # the verification portion of this contract checked it all out
        # but the application part of the contract needs to sync the balance

        # we don't really care what operation is called
        # no matter what we will try to reconcile
        did_withdraw = ReconcileBalances()

        operation = args[0]

        if operation == 'deposit':

            if not did_withdraw:
                deposit = DepositNeo()

                return deposit
            else:

                print("cannot withdraw and deposit at the same time")
                return False

        elif operation == 'balanceOf':

            if len(args) != 2:
                return False

            account = args[1]
            getbalance = BalanceOf(account)

            return getbalance

    return False


def CanWithdrawNeo():

    print("[can withdraw]")

    tx = GetScriptContainer()

    type = GetType(tx)

    print("[can withdraw] got tx type...")

    if type == 209:
        print("[can withdraw] Is invocation!!")

        # this is the contract's address
        sender_addr = GetExecutingScriptHash()

        withdrawal_amount = 0

        receiver_addr = bytearray(0)

        # go through the outputs of the tx
        # and find ones that are neo
        # and also the receiver cannot be the contract ( sender_addr )
        for output in tx.Outputs:
            shash = GetScriptHash(output)

            output_asset_id = GetAssetId(output)

            if output_asset_id == NEO_ASSET_ID:

                output_val = GetValue(output)

                if shash != sender_addr:

                    print("[can withdraw] output is to receiver")
                    receiver_addr = shash

                    withdrawal_amount = withdrawal_amount + output_val

                    Notify(withdrawal_amount)
                    Notify(output)

                else:

                    print("[can withdraw] output is to contract sender addr, subtract from withdraw total")

                    withdrawal_amount = withdrawal_amount - output_val

                    Notify(output)
            else:

                print("[can withdraw] output is not neo")
                Notify(output)

        # we check recevier addr and amount

        if len(receiver_addr) > 0:

            print("[can withdraw] receiver addr is valid")
            Notify(receiver_addr)

            context = GetContext()

            current_balance = Get(context, receiver_addr)

            print("[can withdraw] current balance")
            Notify(current_balance)
            Notify(withdrawal_amount)

            if withdrawal_amount <= current_balance:

                print("[can withdraw] withdrawl amount il less than balance")

                onWithdraw(receiver_addr, withdrawal_amount)

                return True

            else:

                print("[can withdraw] not enough to witdraw")
        else:

            print("[can withdraw] receiver addr not set")
    else:

        print("[can withdraw] tx is not invocation tx. return false")

    return False


def DepositNeo():

    # get reference to the tx the invocation is in
    tx = GetScriptContainer()

    references = tx.References

    if len(references) < 1:
        print("no neo attached")
        return False

    # we need to determine who sent the tx
    reference = references[0]
    sender = GetScriptHash(reference)

    # this will keep track of how much neo was deposited
    value = 0

    output_asset_id = GetAssetId(reference)

    if output_asset_id != NEO_ASSET_ID:
        print("Must deposit NEO")
        return False

    # this is the contract's address
    receiver = GetExecutingScriptHash()

    # go through all the outputs
    # and check if the receiver is the contract
    # if that is true, we add the value of the output to the
    # total sum that was deposited

    for output in tx.Outputs:
        shash = GetScriptHash(output)
        if shash == receiver:
            output_val = GetValue(output)
            value = value + output_val

    if value > 0:

        print("neo was deposited")
        Notify(value)

        # now we know value was deposited from the sender

        context = GetContext()

        # check the current balance of the sender
        current_balance = Get(context, sender)
        print("current balance...")
        Notify(current_balance)

        new_balance = current_balance + value

        print("new balance..")
        Notify(new_balance)

        Put(context, sender, new_balance)

        print("deposited")

        onDeposit(sender, value)

        return True

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

    if len(balance) < 1:
        balance = 0

    return balance


def ReconcileBalances():

    print("[Reconcile balances]")
    # this is the contract's address
    sender_addr = GetExecutingScriptHash()

    tx = GetScriptContainer()

    withdrawal_amount = 0

    receiver_addr = bytearray(0)

    # go through the outputs of the tx
    # and find ones that are neo
    # and also the receiver cannot be the contract ( sender_addr )
    for output in tx.Outputs:
        shash = GetScriptHash(output)

        output_asset_id = GetAssetId(output)

        if output_asset_id == NEO_ASSET_ID:

            if shash != sender_addr:

                print("[reconcile] output is to receiver")
                receiver_addr = shash

                output_val = GetValue(output)

                withdrawal_amount = withdrawal_amount + output_val

                Notify(withdrawal_amount)
                Notify(output)

            else:

                print("[Reconcile balances] output is to contract sender addr, ignore")
                Notify(output)
        else:

            print("[Reconcile balances] output is not neo")
            Notify(output)

    # we check recevier addr and amount

    if len(receiver_addr) > 0:

        print("[Reconcile balances] receiver addr is valid")
        Notify(receiver_addr)

        context = GetContext()

        current_balance = Get(context, receiver_addr)

        print("[Reconcile balances] current balance")
        Notify(current_balance)
        Notify(withdrawal_amount)

        if withdrawal_amount <= current_balance:

            new_balance = current_balance - withdrawal_amount

            print("[Reconcile balances] new balance is...")
            Notify(current_balance)
            Notify(new_balance)

            Put(context, receiver_addr, new_balance)

            onWithdrawReconciled(receiver_addr, new_balance)
            print("[Reconcile balances] withdrawl amount il less than balance")
            return True

        else:

            print("[Reconcile balances] not enough to witdraw")
    else:

        print("[Reconcile balances] receiver addr not set")

    return False
