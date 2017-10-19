

class ExecutionEngine():
    """
    Not used
    """
    pass


def GetScriptContainer():
    """
    Returns the current Script Container of a smart contract execution. This will be
    ``boa.blockchain.vm.Neo.Transaction`` object

    :return: the current ScriptContainer of a smart contract execution.
    :rtype: ``boa.blockchain.vm.Neo.Transaction``

    """
    pass


def GetExecutingScriptHash():
    """
    gets the hash of the script ( smart contract ) which is currently being executed

    - this method is implemented inside the Neo Virtual Machine

    :return: the hash of the script ( smart contract ) which is currently being executed
    :rtype: bytearray

    """
    pass


def GetCallingScriptHash():
    """
    gets the hash of the script ( smart contract ) which began execution of the current script

    :return: the hash of the script ( smart contract ) which began execution of the current script
    :rtype: bytearray

    """
    pass


def GetEntryScriptHash():
    """
    gets the hash of the script ( smart contract ) which began execution of the smart contract

    :return: the hash of the script ( smart contract ) which began execution of the smart contract
    :rtype: bytearray
    """
    pass
