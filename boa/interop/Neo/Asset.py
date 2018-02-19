
class Asset:

    @property
    def AssetId(self):
        """

        :return:
        """
        return GetAssetId(self)

    @property
    def AssetType(self):
        """

        :return:
        """
        return GetAssetType(self)

    @property
    def Amount(self):
        """

        :return:
        """
        return GetAmount(self)

    @property
    def Available(self):
        """

        :return:
        """
        return GetAvailable(self)

    @property
    def Precision(self):
        """

        :return:
        """
        return GetPrecision(self)

    @property
    def Owner(self):
        """

        :return:
        """
        return GetOwner(self)

    @property
    def Admin(self):
        """

        :return:
        """
        return GetAdmin(self)

    @property
    def Issuer(self):
        """

        :return:
        """
        return GetIssuer(self)


def GetAssetId(asset):
    """

    :param asset:
    """
    pass


def GetAssetType(asset):
    """

    :param asset:
    """
    pass


def GetAmount(asset):
    """

    :param asset:
    """
    pass


def GetAvailable(asset):
    """

    :param asset:
    """
    pass


def GetPrecision(asset):
    """

    :param asset:
    """
    pass


def GetOwner(asset):
    """

    :param asset:
    """
    pass


def GetAdmin(asset):
    """

    :param asset:
    """
    pass


def GetIssuer(asset):
    """

    :param asset:
    """
    pass


def Create(asset_type, name, amount, precision, owner, admin, issuer):
    """

    :param asset_type:
    :param name:
    :param amount:
    :param precision:
    :param owner:
    :param admin:
    :param issuer:
    """
    pass


def Renew(asset, years):
    """

    :param asset:
    :param years:
    """
    pass
