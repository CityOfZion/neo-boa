
class TransactionOutput:

    @property
    def AssetId(self):
        """

        :return:
        """
        return GetAssetId(self)

    @property
    def Value(self):
        """

        :return:
        """
        return GetValue(self)

    @property
    def ScriptHash(self):
        """

        :return:
        """
        return GetScriptHash(self)


def GetAssetId(output):
    """

    :param output:
    """
    pass


def GetValue(output):
    """

    :param output:
    """
    pass


def GetScriptHash(output):
    """

    :param output:
    """
    pass
