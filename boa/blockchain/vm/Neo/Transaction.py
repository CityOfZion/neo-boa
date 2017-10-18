
class Transaction():

    @property
    def Hash(self):
        """

        :return:
        """
        return GetHash(self)

    @property
    def Type(self):
        """

        :return:
        """
        return GetType(self)

    @property
    def Attributes(self):
        """

        :return:
        """
        return GetAttributes(self)

    @property
    def Inputs(self):
        """

        :return:
        """
        return GetInputs(self)

    @property
    def Outputs(self):
        """

        :return:
        """
        return GetOutputs(self)

    @property
    def References(self):
        """

        :return:
        """
        return GetReferences(self)


def GetHash(transaction):
    """

    :param transaction:
    """
    pass


def GetType(transaction):
    """

    :param transaction:
    """
    pass


def GetAttributes(transaction):
    """

    :param transaction:
    """
    pass


def GetInputs(transaction):
    """

    :param transaction:
    """
    pass


def GetOutputs(transaction):
    """

    :param transaction:
    """
    pass


def GetReferences(transaction):
    """

    :param transaction:
    """
    pass
