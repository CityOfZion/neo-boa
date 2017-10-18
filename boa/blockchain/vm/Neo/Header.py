

class Header():

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


def GetHash(header):
    """

    :param header:
    """
    pass


def GetVersion(header):
    """

    :param header:
    """
    pass


def GetPrevHash(header):
    """

    :param header:
    """
    pass


def GetMerkleRoot(header):
    """

    :param header:
    """
    pass


def GetTimestamp(header):
    """

    :param header:
    """
    pass


def GetConsensusData(header):
    """

    :param header:
    """
    pass


def GetNextConsensus(header):
    """

    :param header:
    """
    pass
