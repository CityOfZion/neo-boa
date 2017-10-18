from boa.blockchain.vm.Neo.Transaction import Transaction


class Block():

    @property
    def TransactionCount(self):
        """

        :return:
        """
        return GetTransactionCount(self)

    @property
    def Transactions(self):
        """

        :return:
        """
        return GetTransactions(self)


def GetTransactionCount(block) -> int:
    """

    :param block:
    """
    pass


def GetTransactions(block) -> list:
    """

    :param block:
    """
    pass


def GetTransaction(block, index) -> Transaction:
    """

    :param block:
    :param index:
    """
    pass
