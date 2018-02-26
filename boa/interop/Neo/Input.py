
class TransactionInput:

    @property
    def Hash(self):
        """

        :return:
        """
        return GetInputHash(self)

    @property
    def Index(self):
        """

        :return:
        """
        return GetIndex(self)


def GetInputHash(input):
    """

    :param input:
    """
    pass


def GetIndex(input):
    """

    :param input:
    """
    pass
