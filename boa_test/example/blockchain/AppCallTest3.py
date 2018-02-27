from boa.interop.Neo.App import RegisterAppCall

CalculatorContract = RegisterAppCall(b'W\xa7\x18\x08MZh\xbdu\xb7%\x88\x8e\x19J\x9e\xd4|\xe1\xe3\xaa', 'operation', 'a', 'b')


def Main(operation, a, b):

    result = CalculatorContract(operation, a, b)

    return result
