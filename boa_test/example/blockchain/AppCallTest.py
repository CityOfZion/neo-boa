from boa.interop.Neo.App import RegisterAppCall

CalculatorContract = RegisterAppCall('86d58778c8d29e03182f38369f0d97782d303cc0', 'operation', 'a', 'b')


def Main(operation, a, b):

    result = CalculatorContract(operation, a, b)

    return result
