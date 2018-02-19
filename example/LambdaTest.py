

def Main():
    """
    a sample smart contract demonstrating how to use lambdas in smart contracts

    :return: result of the smart contract execution
    :rtype: int

    """
    j = 9

    def q(x):
        """

        :param x:
        :return:
        """
        return x + 1

    m = q(j)

    return m
