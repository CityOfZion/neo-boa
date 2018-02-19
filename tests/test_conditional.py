from unittest import TestCase
from boa.compiler import Compiler
from neo.Implementations.Wallets.peewee.UserWallet import UserWallet
from neo.Prompt.Commands.BuildNRun import TestBuild
from neo.Settings import settings
from neocore.UInt160 import UInt160

from neo.Utils.WalletFixtureTestCase import WalletFixtureTestCase

settings.DEBUG_STORAGE_PATH = './fixtures/debugstorage'

class TestAddContract(WalletFixtureTestCase):


    FIXTURE_REMOTE_LOC = 'https://s3.us-east-2.amazonaws.com/cityofzion/fixtures/fixtures_v5.tar.gz'
    FIXTURE_FILENAME = './fixtures/fixtures_v5.tar.gz'


    wallet_1_script_hash = UInt160(data=b'S\xefB\xc8\xdf!^\xbeZ|z\xe8\x01\xcb\xc3\xac/\xacI)')

    wallet_1_addr = 'APRgMZHZubii29UXF9uFa6sohrsYupNAvx'

    _wallet1 = None

    @classmethod
    def GetWallet1(cls, recreate=False):
        if cls._wallet1 is None or recreate:
            cls._wallet1 = UserWallet.Open(TestAddContract.wallet_1_dest(), TestAddContract.wallet_1_pass())
        return cls._wallet1


    def test_CompareTest0(self):

        output = Compiler.instance().load('example/CompareTest0.py').default
        out = output.write()
        print(output.to_s())

        tx, results, total_ops, engine = TestBuild(out, [2,4], self.GetWallet1(), '0202','02')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger(), 2)

        tx, results, total_ops, engine = TestBuild(out, [4,2], self.GetWallet1(), '0202','02')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger(), 3)

        tx, results, total_ops, engine = TestBuild(out, [2,2], self.GetWallet1(), '0202','02')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger(), 2)

        tx, results, total_ops, engine = TestBuild(out, ['b','a'], self.GetWallet1(), '0202','02')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger(), 3)

        tx, results, total_ops, engine = TestBuild(out, ['a','b'], self.GetWallet1(), '0202','02')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger(), 2)

    def test_CompareTest2(self):

        output = Compiler.instance().load('example/CompareTest2.py').default
        out = output.write()
        print(output.to_s())

        tx, results, total_ops, engine = TestBuild(out, [2,2], self.GetWallet1(), '0202','01')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBoolean(), True)

        tx, results, total_ops, engine = TestBuild(out, [2,3], self.GetWallet1(), '0202','01')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBoolean(), False)

