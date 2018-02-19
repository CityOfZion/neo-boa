from unittest import TestCase
from boa.compiler import Compiler
from neo.Implementations.Wallets.peewee.UserWallet import UserWallet
from neo.Prompt.Commands.BuildNRun import TestBuild
from neo.Settings import settings
from neocore.UInt160 import UInt160

from neo.Utils.WalletFixtureTestCase import WalletFixtureTestCase

settings.DEBUG_STORAGE_PATH = './fixtures/debugstorage'

class TestMethodContracts(WalletFixtureTestCase):


    FIXTURE_REMOTE_LOC = 'https://s3.us-east-2.amazonaws.com/cityofzion/fixtures/fixtures_v5.tar.gz'
    FIXTURE_FILENAME = './fixtures/fixtures_v5.tar.gz'


    wallet_1_script_hash = UInt160(data=b'S\xefB\xc8\xdf!^\xbeZ|z\xe8\x01\xcb\xc3\xac/\xacI)')

    wallet_1_addr = 'APRgMZHZubii29UXF9uFa6sohrsYupNAvx'

    _wallet1 = None

    @classmethod
    def GetWallet1(cls, recreate=False):
        if cls._wallet1 is None or recreate:
            cls._wallet1 = UserWallet.Open(TestMethodContracts.wallet_1_dest(), TestMethodContracts.wallet_1_pass())
        return cls._wallet1


    def test_Method1(self):

        output = Compiler.instance().load('example/MethodTest.py').default
        out = output.write()
#        print("out %s " % output.to_s())
        tx, results, total_ops, engine = TestBuild(out, [1,2], self.GetWallet1(), '0202','02')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger(), 7)

        tx, results, total_ops, engine = TestBuild(out, [-3, -100], self.GetWallet1(), '0202','02')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger(), -99)


    def test_Method2(self):

        output = Compiler.instance().load('example/MethodTest2.py').default
        out = output.write()
#        print("out %s " % output.to_s())
        tx, results, total_ops, engine = TestBuild(out, [], self.GetWallet1(), '','02')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger(), 26)

    def test_MethodTest4(self):
        output = Compiler.instance().load('example/MethodTest4.py').default
        out = output.write()
        #        print("out %s " % output.to_s())
        tx, results, total_ops, engine = TestBuild(out, [], self.GetWallet1(), '', '02')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger(), 63)
