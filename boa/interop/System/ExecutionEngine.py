

def GetScriptContainer():
    """
    Return the current Script Container of a smart contract execution. 
    This will be a ``boa.blockchain.vm.Neo.Transaction`` object.

    - Note: This method is implemented inside the Neo Virtual Machine.

    :return: the current ScriptContainer of a smart contract execution.
    :rtype: ``boa.blockchain.vm.Neo.Transaction``
    """

    pass


def GetExecutingScriptHash():
    """
    Get the hash of the script ( smart contract ) which is currently being executed

    - Note: This method is implemented inside the Neo Virtual Machine.

    :return: the hash of the script ( smart contract ) which is currently being executed
    :rtype: bytearray
    """

    pass


def GetCallingScriptHash():
    """
    Get the hash of the script ( smart contract ) which began execution of the current script.

    - Note: This method is implemented inside the Neo Virtual Machine.

    :return: the hash of the script ( smart contract ) which began execution of the current script
    :rtype: bytearray
    """

    pass


def GetEntryScriptHash():
    """
    Get the hash of the script ( smart contract ) which began execution of the smart contract.

    - Note: This method is implemented inside the Neo Virtual Machine.

    :return: the hash of the script ( smart contract ) which began execution of the smart contract
    :rtype: bytearray
    """

    pass
