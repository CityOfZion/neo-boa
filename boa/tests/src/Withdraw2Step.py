from boa.blockchain.vm.Neo.Runtime import Notify,GetTrigger,CheckWitness
from boa.blockchain.vm.Neo.Action import RegisterAction
from boa.blockchain.vm.Neo.TriggerType import Application,Verification

from boa.blockchain.vm.Neo.TransactionType import InvocationTransaction
from boa.blockchain.vm.Neo.Transaction import *

from boa.blockchain.vm.System.ExecutionEngine import GetScriptContainer,GetExecutingScriptHash,GetCallingScriptHash,GetEntryScriptHash

from boa.blockchain.vm.Neo.Output import GetScriptHash, GetValue, GetAssetId
from boa.blockchain.vm.Neo.Storage import GetContext, Get, Put, Delete

from boa.code.builtins import range,concat,list

OWNER= b'\x13\xff4\xcc\x10\x1cVs\x7fe\xc3\xb3\xd2\xf9iTHESK'

NEO_ASSET_ID = b'\x9b|\xff\xda\xa6t\xbe\xae\x0f\x93\x0e\xbe`\x85\xaf\x90\x93\xe5\xfeV\xb3J\\"\x0c\xcd\xcfn\xfc3o\xc5'


onDeposit = RegisterAction('deposit','account','amount')

onWithdrawRequestApproved = RegisterAction('withdrawApproved','account','vin_tx_id','vin_index')


def Main(operation,args):

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
            print("CLEARED?")
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
        onDeposit(sender,value)

        return True

    return False


def VerifyWithdrawalRequest(args):

    account = args[0]

    if CheckHasPendingWithdrawal(account):
        print("already a pending withdrawal")
        return False

    arglen = len(args)

    txids_len = arglen / 2


    output = None

    for i in range(0, txids_len):

        j = i * 2
        vin_tx = args[j + 1]
        vin_index = args[j + 2]

        can_withdraw = PlaceVINHold(account, vin_tx,vin_index)

        if can_withdraw:

            onWithdrawRequestApproved(account,vin_tx,vin_index)

            vin = concat(vin_index,vin_tx)

            if len(output) > 1:
                output = concat(output,vin)
            else:
                output = vin

        else:
            print("cant withdraw")

    save = SetPendingWithdrawal(account, output)

    return output

def GetSender():

    # get reference to the tx the invocation is in
    tx = GetScriptContainer()

    m = GetCallingScriptHash()
    Notify(m)
    return 'aouaoeu'

def CheckHasPendingWithdrawal(account):

    context = GetContext()

    account_has_pending= concat(account,'pending')

    pending = Get(context, account_has_pending)

    if pending > 0:

        return True

    print("no pending withdrawal yet!")
    return False

def SetPendingWithdrawal(account, value):

    context = GetContext()

    account_has_pending = concat(account, 'pending')

    if value == '':

        Delete(context,account_has_pending)

    else:

        Put(context,account_has_pending,value)

    return True


def GetPendingWithdrawal(account):
    print("looking up pending witdrawal!")
    context = GetContext()

    account_pending = concat(account,'pending')

    result = Get(context, account_pending)

    return result


def DeletePendingWithdrawal(account):

    context = GetContext()
    account_pending = concat(account,'pending')

    Delete(context, account_pending)
    print("cleared?")
    return True

def PlaceVINHold( account, txid, index):

    context = GetContext()

    hold_id= concat(index,txid)

    item = Get(context, hold_id)

    if len(item) < 1:
        Put(context, hold_id, account)
        return True

    elif item == account:
        print("existing hold for account")
        return True

    return False