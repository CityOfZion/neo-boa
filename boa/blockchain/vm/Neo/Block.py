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


def GetTransactionCount(block :Block) -> int:
    """

    returns the number of transactions in a block


    """
    pass


def GetTransactions(block: Block) -> list:
    """
    returns a list of transactions contained in a block


    """
    pass


def GetTransaction(block: Block, index:int) -> Transaction:
    """

    :param block: the block to get the transaction from
    :param index: the index of the transaction within the lock


    """

    pass
