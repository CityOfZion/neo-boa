

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


def GetHash(header: Header) -> bytearray:
    """

    gets the hash of the header

    """
    pass


def GetVersion(header: Header) -> int:
    """

    gets the version of the header

    """
    pass


def GetPrevHash(header: Header) -> bytearray:
    """

    gets the hash of the previous header in the blockchain

    """
    pass


def GetMerkleRoot(header: Header) -> bytearray:
    """

    gets the merkle root of the transactions contained in the block

    """
    pass


def GetTimestamp(header: Header) -> int:
    """

    gets the timestamp of when the header was created

    """
    pass


def GetConsensusData(header: Header) -> bytearray:
    """

    gets the address of the consensus

    """
    pass


def GetNextConsensus(header: Header) -> bytearray:
    """

    gets the address where the next consensus will occur

    """
    pass
