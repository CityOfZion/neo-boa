from neo.Implementations.Wallets.peewee.UserWallet import UserWallet
from neo.Settings import settings
from neocore.UInt160 import UInt160
from neo.Wallets.utils import to_aes_key

from neo.Utils.WalletFixtureTestCase import WalletFixtureTestCase

settings.USE_DEBUG_STORAGE = False
# settings.DEBUG_STORAGE_PATH = './fixtures/debugstorage'


class BoaTest(WalletFixtureTestCase):

    FIXTURE_REMOTE_LOC = 'https://s3.us-east-2.amazonaws.com/cityofzion/fixtures/fixtures_v5.tar.gz'
    FIXTURE_FILENAME = './fixtures/empty_fixture.tar.gz'

    wallet_1_script_hash = UInt160(data=b'S\xefB\xc8\xdf!^\xbeZ|z\xe8\x01\xcb\xc3\xac/\xacI)')

    wallet_1_addr = 'APRgMZHZubii29UXF9uFa6sohrsYupNAvx'

    _wallet1 = None

    @classmethod
    def GetWallet1(cls, recreate=False):
        if cls._wallet1 is None or recreate:
            cls._wallet1 = UserWallet.Open(BoaTest.wallet_1_dest(), to_aes_key(BoaTest.wallet_1_pass()))
        return cls._wallet1


class BoaFixtureTest(WalletFixtureTestCase):

    FIXTURE_REMOTE_LOC = 'https://s3.us-east-2.amazonaws.com/cityofzion/fixtures/fixtures_v5.tar.gz'
    FIXTURE_FILENAME = './fixtures/fixtures_v5.tar.gz'

    wallet_1_script_hash = UInt160(data=b'S\xefB\xc8\xdf!^\xbeZ|z\xe8\x01\xcb\xc3\xac/\xacI)')

    wallet_1_addr = 'APRgMZHZubii29UXF9uFa6sohrsYupNAvx'

    _wallet1 = None

    wallet_2_script_hash = UInt160(data=b'4\xd0=k\x80TF\x9e\xa8W\x83\xfa\x9eIv\x0b\x9bs\x9d\xb6')

    wallet_2_addr = 'ALb8FEhEmtSqv97fuNVuoLmcmrSKckffRf'

    _wallet2 = None

    @classmethod
    def GetWallet1(cls, recreate=False):
        if cls._wallet1 is None or recreate:
            cls._wallet1 = UserWallet.Open(BoaFixtureTest.wallet_1_dest(), to_aes_key(BoaFixtureTest.wallet_1_pass()))
        return cls._wallet1

    @classmethod
    def GetWallet2(cls, recreate=False):
        if cls._wallet2 is None or recreate:
            cls._wallet2 = UserWallet.Open(BoaFixtureTest.wallet_2_dest(), to_aes_key(BoaFixtureTest.wallet_2_pass()))
        return cls._wallet2
