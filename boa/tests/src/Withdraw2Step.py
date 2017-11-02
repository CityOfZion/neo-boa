from boa.blockchain.vm.Neo.Runtime import Notify, GetTrigger, CheckWitness
from boa.blockchain.vm.Neo.Action import RegisterAction
from boa.blockchain.vm.Neo.TriggerType import Application, Verification
from boa.blockchain.vm.Neo.Blockchain import GetTransaction
from boa.blockchain.vm.Neo.TransactionType import InvocationTransaction
from boa.blockchain.vm.Neo.Transaction import *

from boa.blockchain.vm.System.ExecutionEngine import GetScriptContainer, GetExecutingScriptHash, GetCallingScriptHash, GetEntryScriptHash

from boa.blockchain.vm.Neo.Output import GetScriptHash, GetValue, GetAssetId
from boa.blockchain.vm.Neo.Input import GetHash, GetIndex
from boa.blockchain.vm.Neo.Storage import GetContext, Get, Put, Delete

from boa.code.builtins import range, concat, list, print_var

OWNER = b'\xaf\x12\xa8h{\x14\x94\x8b\xc4\xa0\x08\x12\x8aU\nci[\xc1\xa5'

NEO_ASSET_ID = b'\x9b|\xff\xda\xa6t\xbe\xae\x0f\x93\x0e\xbe`\x85\xaf\x90\x93\xe5\xfeV\xb3J\\"\x0c\xcd\xcfn\xfc3o\xc5'


onDeposit = RegisterAction('deposit', 'account', 'amount')

onWithdrawRequestApproved = RegisterAction('withdrawApproved', 'account', 'vin_requests')


def Main(operation, args):

    trigger = GetTrigger()

    if trigger == b'\x00':

        print("doing verification")

        # always allow owner to withdraw
        # this should be changed
        # to not allow the owner to withdraw from
        # vins that are earmarked for others
        if CheckWitness(OWNER):
            return True
        else:

            # if it is not the owner, we need to verify a few things
            can_widthraw = CanWithdraw()

            return can_widthraw

    elif trigger == b'\x10':

        if operation == 'deposit':

            deposit = DepositNeo()
            return deposit

        elif operation == 'withdrawalRequest':

            withdrawable_txs = VerifyWithdrawalRequest(args)
            return withdrawable_txs

        elif operation == 'getPending':
            account = args[0]
            withdrawable_txs = GetPendingWithdrawal(account)
            return withdrawable_txs

        elif operation == 'clearPending':
            account = args[0]
            result = DeletePendingWithdrawal(account)
            return result

        elif operation == 'balanceOf':
            account = args[0]
            result = BalanceOf(account)
            return result

        else:

            return 'unknown operation'

    return False


def CanWithdraw():

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

    # this is the contract's address
    receiver = GetExecutingScriptHash()

    # go through all the outputs
    # and check if the receiver is the contract
    # if that is true, we add the value of the output to the
    # total sum that was deposited

    for output in tx.Outputs:
        shash = GetScriptHash(output)
        if shash == receiver:

            output_asset_id = GetAssetId(output)

            if output_asset_id == NEO_ASSET_ID:

                output_val = GetValue(output)
                value = value + output_val

    if value > 0:

        # now we know value was deposited from the sender

        # check the current balance of the sender
        # add it to the deposit amount, and save
        context = GetContext()
        current_balance = Get(context, sender)
        new_balance = current_balance + value
        Put(context, sender, new_balance)

        # send deposit event
        onDeposit(sender, value)

        return True

    return False


def VerifyWithdrawalRequest(args):

    account = args[0]

    current_balance = BalanceOf(account)

    if current_balance == 0:
        print("No Current balance")
        return False

    if CheckHasPendingWithdrawal(account):
        print("already a pending withdrawal")
        return False

    arglen = len(args)

    txids_len = arglen / 2

    vin_requests = list(length=txids_len)

    # so, this is a bit involved, so bear with me here
    # lets assume a person has a balance that the contract owes them
    # we need to allow them to put a hold on some tx vins that they can 'claim'
    # after they have put the hold on them, they can withdraw and in the
    # verification portion of the contract it will allow them

    # but they may need to put a hold on tx vins that have a value
    # more than they are owed.  So we want to allow them to put a hold
    # on x number of txids, where the amount contained in x-1 vins is less than the amount they are owed
    # and the amount in x txids is greater than or equal to the amount they are owed
    # but only by one

    hold_amount = 0
    okcount = 0

    for i in range(0, txids_len):

        j = i * 2

        request_vin_tx = args[j + 1]
        request_vin_index = args[j + 2]

        vin = LookupVIN(request_vin_tx, request_vin_index)

        if vin and vin[1] == NEO_ASSET_ID:

            actual_amount = vin[0]

            # if the amount being held is less than the current balance
            # it is ok, we allow the vin request
            # this allows the hold amount to go over
            # but if it is too much then invalidate
            # the entire request

            if hold_amount < current_balance:
                hold_amount += actual_amount

                vin_request = [request_vin_tx, request_vin_index]
                vin_requests[i] = vin_request
                okcount += 1

    if okcount != txids_len:
        print("Invalid txid request")
        return False

    Notify(hold_amount)
    Notify(current_balance)

    # now that we've checked the requestor isn't requesting too much
    # we will check that the requestor can put a hold on the vins
    # we make sure they can put a hold on all the vins
    # before actually placing the hold on the vin
    for vin in vin_requests:

        vin_tx = vin[0]
        vin_index = vin[1]

        has_hold = HasVINHold(vin_tx, vin_index)

        if has_hold:
            print("Cannot request withdrawal, vin(s) already have hold")
            return False

    # now that we're sure we can put holds on all the requested vins
    # we will put holds on the requested vins

    output = None

    for vin in vin_requests:
        vin_tx = vin[0]
        vin_index = vin[1]

        hold_req = PlaceVINHold(account, vin_tx, vin_index)

        # now we assemble a bytearray
        # to save to storage
        vin = concat(vin_index, vin_tx)

        if len(output) > 1:
            output = concat(output, vin)
        else:
            output = vin

    onWithdrawRequestApproved(account, vin_requests)

    m = SetPendingWithdrawal(account, output)

    return vin_requests


def BalanceOf(account):
    """
    Method to return the current balance of an address

    :param account: the account address to retrieve the balance for
    :type account: bytearray

    :return: the current balance of an address
    :rtype: int

    """
    context = GetContext()
    balance = Get(context, account)

    return balance


def CheckHasPendingWithdrawal(account):

    context = GetContext()

    account_has_pending = concat(account, 'pending')

    pending = Get(context, account_has_pending)

    return pending


def SetPendingWithdrawal(account, value):

    context = GetContext()

    account_has_pending = concat(account, 'pending')

    if value == 0:

        Delete(context, account_has_pending)

    else:

        Put(context, account_has_pending, value)

    return True


def GetPendingWithdrawal(account):

    context = GetContext()

    account_pending = concat(account, 'pending')

    result = Get(context, account_pending)

    return result


def DeletePendingWithdrawal(account):

    context = GetContext()
    account_pending = concat(account, 'pending')

    Delete(context, account_pending)

    return True


def HasVINHold(txid, index):

    context = GetContext()
    hold_id = concat(txid, index)

    item = Get(context, hold_id)

    return item


def PlaceVINHold(account, txid, index):

    context = GetContext()

    hold_id = concat(index, txid)

    Put(context, hold_id, account)

    return True


def GetTXInputs():

    tx = GetScriptContainer()

    inputs = tx.Inputs
    inputlen = len(inputs)

    results = list(length=inputlen)

    count = 0

    for input in tx.Inputs:

        txid = GetHash(input)
        index = GetIndex(input)
        item = [txid, index]
        results[count] = item
        count += 1

    return results


def LookupVIN(txid, index):

    tx = GetTransaction(txid)

    if tx:

        outputs = tx.Outputs

        output_len = len(outputs)

        if index < output_len:

            output = outputs[index]

            assetType = GetAssetId(output)
            assetAmount = GetValue(output)
            toret = [assetAmount, assetType]
            return toret

    print("could not lookup vin. TX or output not found")
    return False
