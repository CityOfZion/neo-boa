from boa.interop.Neo.Header import GetIndex, GetHash, GetPrevHash, GetTimestamp, GetVersion, GetNextConsensus, GetMerkleRoot, GetConsensusData


class Block:

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

    @property
    def Index(self):
        """

        Returns:

        """
        return GetIndex(self)

    @property
    def Hash(self):
        """

        :return:
        """
        return GetHash(self)

    @property
    def Timestamp(self):
        """

        :return:
        """
        return GetTimestamp(self)

    @property
    def Version(self):
        """

        :return:
        """
        return GetVersion(self)

    @property
    def PrevHash(self):
        """

        :return:
        """
        return GetPrevHash(self)

    @property
    def MerkleRoot(self):
        """

        :return:
        """
        return GetMerkleRoot(self)

    @property
    def ConsensusData(self):
        """

        :return:
        """
        return GetConsensusData(self)

    @property
    def NextConsensus(self):
        """

        :return:
        """
        return GetNextConsensus(self)


def GetTransactionCount(block):
    """

    returns the number of transactions in a block


    """
    pass


def GetTransactions(block):
    """
    returns a list of transactions contained in a block


    """
    pass


def GetTransaction(block, index):
    """

    :param block: the block to get the transaction from
    :param index: the index of the transaction within the lock


    """

    pass
