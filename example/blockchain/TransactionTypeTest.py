# tested

from boa.interop.Neo.TransactionType import *


def Main(operation):
    """
        MinerTransaction = b'\x00'
        IssueTransaction = b'\x01'
        ClaimTransaction = b'\x02'
        EnrollmentTransaction = b'\x20'
        VotingTransaction = b'\x24'
        RegisterTransaction = b'\x40'
        ContractTransaction = b'\x80'
        StateTransaction = b'\x90'
        AgencyTransaction = b'\xb0'
        PublishTransaction = b'\xd0'
        InvocationTransaction = b'\xd1'
    """

    if operation == 'miner':
        return MinerTransaction()

    elif operation == 'issue':
        return IssueTransaction()

    elif operation == 'claim':
        return ClaimTransaction()

    elif operation == 'enrollment':
        return EnrollmentTransaction()

    elif operation == 'voting':
        return VotingTransaction()

    elif operation == 'register':
        return RegisterTransaction()

    elif operation == 'contract':
        return ContractTransaction()

    elif operation == 'state':
        return StateTransaction()

    elif operation == 'agency':
        return AgencyTransaction()

    elif operation == 'publish':
        return PublishTransaction()

    elif operation == 'invocation':
        return InvocationTransaction()

    return 'unknown operation'
