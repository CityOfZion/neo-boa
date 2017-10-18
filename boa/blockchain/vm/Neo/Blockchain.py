from boa.blockchain.vm.Neo.Header import *
from boa.blockchain.vm.Neo.Block import *
from boa.blockchain.vm.Neo.Transaction import *
from boa.blockchain.vm.Neo.Account import *
from boa.blockchain.vm.Neo.Asset import *
from boa.blockchain.vm.Neo.Contract import *


def GetHeight() -> int:
    """

    """
    pass


def GetHeader(height_or_hash) -> Header:
    """

    :param height_or_hash:
    """
    pass


def GetBlock(height_or_hash) -> Block:
    """

    :param height_or_hash:
    """
    pass


def GetTransaction(hash) -> Transaction:
    """

    :param hash:
    """
    pass


def GetAccount(script_hash) -> Account:
    """

    :param script_hash:
    """
    pass


def GetValidators() -> []:
    """

    """
    pass


def GetAsset(asset_id) -> Asset:
    """

    :param asset_id:
    """
    pass


def GetContract(script_hash) -> Contract:
    """

    :param script_hash:
    """
    pass
