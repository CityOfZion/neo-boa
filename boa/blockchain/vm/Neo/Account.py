
class Account:

    @property
    def ScriptHash(self):
        """

        :return:
        """
        return GetScriptHash(self)

    @property
    def Votes(self):
        """

        :return:
        """
        return GetVotes(self)


def GetScriptHash(account):
    """

    :param account:
    """
    pass


def GetVotes(account):
    """

    :param account:
    """
    pass


def SetVotes(account, votes):
    """

    :param account:
    :param votes:
    """
    pass


def GetBalance(account, asset_id):
    """

    :param account:
    :param asset_id:
    """
    pass
