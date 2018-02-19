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


    def test_AddTest(self):

        output = Compiler.instance().load('example/AddTest.py').default.write()

        tx, results, total_ops, engine = TestBuild(output, [2], self.GetWallet1(), '02','02')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger(), 4)

        tx, results, total_ops, engine = TestBuild(output, [23234], self.GetWallet1(), '02','02')
        self.assertEqual(results[0].GetBigInteger(), 23236)

        tx, results, total_ops, engine = TestBuild(output, [0], self.GetWallet1(), '02','02')
        self.assertEqual(results[0].GetBigInteger(), 2)

        tx, results, total_ops, engine = TestBuild(output, [-112], self.GetWallet1(), '02','02')
        self.assertEqual(results[0].GetBigInteger(), -110)


    def test_AddTest1(self):

        output = Compiler.instance().load('example/AddTest1.py').default.write()

        tx, results, total_ops, engine = TestBuild(output, [1,2,3,4], self.GetWallet1(), '02020202','02')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger(), 9)

        tx, results, total_ops, engine = TestBuild(output, [0,0,0,2], self.GetWallet1(), '02020202','02')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger(), 2)

        tx, results, total_ops, engine = TestBuild(output, [-2, 3, -6, 2], self.GetWallet1(), '02020202','02')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger(), -2)

    def test_AddTest2(self):

        output = Compiler.instance().load('example/AddTest2.py').default.write()

        tx, results, total_ops, engine = TestBuild(output, [], self.GetWallet1(), '','02')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger(), 3)


    def test_AddTest4(self):

        output = Compiler.instance().load('example/AddTest4.py').default.write()

        tx, results, total_ops, engine = TestBuild(output, [1,2,3,4], self.GetWallet1(), '','02')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger(), -9)


    def test_AddVoid(self):

        output = Compiler.instance().load('example/AddTestVoid.py').default
        out = output.write()

        tx, results, total_ops, engine = TestBuild(out, [3], self.GetWallet1(), '02','ff')
        # this should I guess return nothing
        # for now it returns an empty byte array
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetByteArray(), bytearray(b'\x00'))

    def test_InplaceMath(self):

        output = Compiler.instance().load('example/InPlaceMath.py').default
        out = output.write()

        tx, results, total_ops, engine = TestBuild(out, [], self.GetWallet1(), '','02')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger(), 21)

