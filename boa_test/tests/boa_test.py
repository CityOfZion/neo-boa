from neo.Implementations.Wallets.peewee.UserWallet import UserWallet
from neo.Settings import settings
from neocore.UInt160 import UInt160
from neo.Wallets.utils import to_aes_key
import os
from neo.Utils.WalletFixtureTestCase import WalletFixtureTestCase

settings.USE_DEBUG_STORAGE = False
# settings.DEBUG_STORAGE_PATH = './fixtures/debugstorage'


class BoaTest(WalletFixtureTestCase):

    dirname = None

    FIXTURE_REMOTE_LOC = 'https://s3.us-east-2.amazonaws.com/cityofzion/fixtures/fixtures_v8.tar.gz'
    FIXTURE_FILENAME = 'fixtures/empty_fixture.tar.gz'

    wallet_1_script_hash = UInt160(data=b'S\xefB\xc8\xdf!^\xbeZ|z\xe8\x01\xcb\xc3\xac/\xacI)')

    wallet_1_addr = 'APRgMZHZubii29UXF9uFa6sohrsYupNAvx'

    _wallet1 = None

    @classmethod
    def setUpClass(cls):

        cls.dirname = '/'.join(os.path.abspath(__file__).split('/')[:-3])

        super(BoaTest, cls).setUpClass()

    @classmethod
    def GetWallet1(cls, recreate=False):
        if cls._wallet1 is None or recreate:
            cls._wallet1 = UserWallet.Open(BoaTest.wallet_1_dest(), to_aes_key(BoaTest.wallet_1_pass()))
        return cls._wallet1


class BoaFixtureTest(WalletFixtureTestCase):

    dirname = None

    FIXTURE_REMOTE_LOC = 'https://s3.us-east-2.amazonaws.com/cityofzion/fixtures/fixtures_v8.tar.gz'
    FIXTURE_FILENAME = './fixtures/fixtures_v8.tar.gz'

    wallet_1_script_hash = UInt160(data=b'\x1c\xc9\xc0\\\xef\xff\xe6\xcd\xd7\xb1\x82\x81j\x91R\xec!\x8d.\xc0')

    wallet_1_addr = 'AJQ6FoaSXDFzA6wLnyZ1nFN7SGSN2oNTc3'

    _wallet1 = None

    wallet_2_script_hash = UInt160(data=b'\x08t/\\P5\xac-\x0b\x1c\xb4\x94tIyBu\x7f1*')

    wallet_2_addr = 'AGYaEi3W6ndHPUmW7T12FFfsbQ6DWymkEm'

    _wallet2 = None

    wallet_3_script_hash = UInt160(data=b'\xc4\xc1\xb0\xcf\xa8\x7f\xcb\xacE\x98W0\x16d\x11\x03]\xdf\xed#')

    wallet_3_addr = 'AZiE7xfyJALW7KmADWtCJXGGcnduYhGiCX'

    _wallet3 = None

    @classmethod
    def setUpClass(cls):
        super(BoaFixtureTest, cls).setUpClass()
        cls.dirname = '/'.join(os.path.abspath(__file__).split('/')[:-3])

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

    @classmethod
    def GetWallet3(cls, recreate=False):
        if cls._wallet3 is None or recreate:
            cls._wallet3 = UserWallet.Open(BoaFixtureTest.wallet_3_dest(), to_aes_key(BoaFixtureTest.wallet_3_pass()))
        return cls._wallet3
