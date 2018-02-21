from neo.Implementations.Wallets.peewee.UserWallet import UserWallet
from neo.Settings import settings
from neo.EventHub import events
from neo.SmartContract.SmartContractEvent import SmartContractEvent
from neocore.UInt160 import UInt160

from neo.Utils.WalletFixtureTestCase import WalletFixtureTestCase

settings.USE_DEBUG_STORAGE = False
#settings.DEBUG_STORAGE_PATH = './fixtures/debugstorage'



class BoaTest(WalletFixtureTestCase):

    FIXTURE_REMOTE_LOC = 'https://s3.us-east-2.amazonaws.com/cityofzion/fixtures/fixtures_v5.tar.gz'
    FIXTURE_FILENAME = './fixtures/empty_fixture.tar.gz'

    wallet_1_script_hash = UInt160(data=b'S\xefB\xc8\xdf!^\xbeZ|z\xe8\x01\xcb\xc3\xac/\xacI)')

    wallet_1_addr = 'APRgMZHZubii29UXF9uFa6sohrsYupNAvx'

    _wallet1 = None

    @classmethod
    def GetWallet1(cls, recreate=False):
        if cls._wallet1 is None or recreate:
            cls._wallet1 = UserWallet.Open(BoaTest.wallet_1_dest(), BoaTest.wallet_1_pass())
        return cls._wallet1


class BoaFixtureTest(WalletFixtureTestCase):

    FIXTURE_REMOTE_LOC = 'https://s3.us-east-2.amazonaws.com/cityofzion/fixtures/fixtures_v5.tar.gz'
    FIXTURE_FILENAME = './fixtures/fixtures_v5.tar.gz'

    wallet_1_script_hash = UInt160(data=b'S\xefB\xc8\xdf!^\xbeZ|z\xe8\x01\xcb\xc3\xac/\xacI)')

    wallet_1_addr = 'APRgMZHZubii29UXF9uFa6sohrsYupNAvx'

    _wallet1 = None

    @classmethod
    def GetWallet1(cls, recreate=False):
        if cls._wallet1 is None or recreate:
            cls._wallet1 = UserWallet.Open(BoaFixtureTest.wallet_1_dest(), BoaFixtureTest.wallet_1_pass())
        return cls._wallet1

