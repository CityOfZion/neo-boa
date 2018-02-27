from boa.interop.Neo.App import RegisterAppCall

CalculatorContract = RegisterAppCall('9e17cd49e4a198e8825b775bd685a4d0818a757', 'operation', 'a', 'b')


def Main(operation, a, b):

    result = CalculatorContract(operation, a, b)

    return result
