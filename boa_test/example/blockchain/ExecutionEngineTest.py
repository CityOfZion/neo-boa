from boa.interop.System.ExecutionEngine import *


def Main(operation):

    if operation == 'executing_sh':
        return GetExecutingScriptHash()

    elif operation == 'script_container':
        return GetScriptContainer()

    elif operation == 'calling_sh':
        return GetCallingScriptHash()

    elif operation == 'entry_sh':
        return GetEntryScriptHash()

    return 'unknown'
