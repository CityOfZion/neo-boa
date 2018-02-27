from boa_test.tests.boa_test import BoaFixtureTest
from boa.compiler import Compiler
from neo.Core.TX.Transaction import Transaction
from neo.Prompt.Commands.BuildNRun import TestBuild


class TestContract(BoaFixtureTest):

    def test_Appcall1(self):

        with self.assertRaises(Exception):
            Compiler.instance().load('%s/boa_test/example/blockchain/AppCallTest2.py' % TestContract.dirname).default

        with self.assertRaises(Exception):
            Compiler.instance().load('%s/boa_test/example/blockchain/AppCallTest3.py' % TestContract.dirname).default

    def test_Appcall2(self):

        output = Compiler.instance().load('%s/boa_test/example/blockchain/AppCallTest.py' % TestContract.dirname).default
        out = output.write()

        tx, results, total_ops, engine = TestBuild(out, ['add', 3, 5], self.GetWallet1(), '070202', '02')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger(), 8)

        tx, results, total_ops, engine = TestBuild(out, ['sub', 3, 5], self.GetWallet1(), '070202', '02')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger(), -2)

        tx, results, total_ops, engine = TestBuild(out, ['mul', 3, 5], self.GetWallet1(), '070202', '02')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger(), 15)

        tx, results, total_ops, engine = TestBuild(out, ['notfound', 3, 5], self.GetWallet1(), '070202', '02')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger(), 0)

    def test_DynamicAppcall(self):

        output = Compiler.instance().load('%s/boa_test/example/blockchain/DynamicAppCallTest.py' % TestContract.dirname).default
        out = output.write()

        tx, results, total_ops, engine = TestBuild(out, [bytearray(b'W\xa7\x18\x08MZh\xbdu\xb7%\x88\x8e\x19J\x9e\xd4|\xe1\xe9'), 'add', 3, 5], self.GetWallet1(), '05070202', '02', dynamic=True)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger(), 8)

        tx, results, total_ops, engine = TestBuild(out, [bytearray(b'W\xa7\x18\x08MZh\xbdu\xb7%\x88\x8e\x19J\x9e\xd4|\xe1\xe9'), 'sub', 3, 5], self.GetWallet1(), '05070202', '02', dynamic=True)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger(), -2)

        tx, results, total_ops, engine = TestBuild(out, [bytearray(b'W\xa7\x18\x08MZh\xbdu\xb7%\x88\x8e\x19J\x9e\xd4|\xe1\xe9'), 'mul', 3, 5], self.GetWallet1(), '05070202', '02', dynamic=True)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger(), 15)

        tx, results, total_ops, engine = TestBuild(out, [bytearray(b'W\xa7\x18\x08MZh\xbdu\xb7%\x88\x8e\x19J\x9e\xd4|\xe1\xe3'), 'add', 3, 5], self.GetWallet1(), '05070202', '02', dynamic=True)
        self.assertEqual(len(results), 0)
#        self.assertEqual(results[0].GetBigInteger(), 0)
