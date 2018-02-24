
class Contract:

    @property
    def Script(self):
        """

        :return:
        """
        return GetScript(self)

    @property
    def StorageContext(self):
        """

        :return:
        """
        return GetStorageContext(self)


def GetScript(contract):
    """

    :param contract:
    """
    pass


def GetStorageContext(contract):
    """

    :param contract:
    """
    pass


def Create(script, parameter_list, return_type, properties, name, version, author, email, description):
    """

    :param script:
    :param parameter_list:
    :param return_type:
    :param properties:
    :param name
    :param version:
    :param author:
    :param email:
    :param description:
    """
    pass


def Migrate(script, parameter_list, return_type, properties, name, version, author, email, description):
    """

    :param script:
    :param parameter_list:
    :param return_type:
    :param need_storage:
    :param name
    :param version:
    :param author:
    :param email:
    :param description:
    """
    pass


def Destroy():
    """

    :param contract:
    """
    pass
