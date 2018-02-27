from boa_test.tests.boa_test import BoaFixtureTest
from boa.compiler import Compiler
from neo.Core.TX.Transaction import Transaction
from neo.Prompt.Commands.BuildNRun import TestBuild


class TestContract(BoaFixtureTest):

    def test_Account(self):

        output = Compiler.instance().load('%s/boa_test/example/blockchain/AccountTest.py' % TestContract.dirname).default
        out = output.write()
        print(output.to_s())

        account = bytearray(b'S\xefB\xc8\xdf!^\xbeZ|z\xe8\x01\xcb\xc3\xac/\xacI)')

        bad_account = bytearray(b'S\xefB\xc8\xdf!^\xbeZ|z\xe8\x01\xcb\xc3\xac/\xacE)')

        tx, results, total_ops, engine = TestBuild(out, ['get_hash', bad_account], self.GetWallet1(), '07', '05')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBoolean(), False)

        tx, results, total_ops, engine = TestBuild(out, ['get_hash', account], self.GetWallet1(), '07', '05')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetByteArray(), account)

        tx, results, total_ops, engine = TestBuild(out, ['get_votes', account], self.GetWallet1(), '07', '05')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetArray(), [])

        tx, results, total_ops, engine = TestBuild(out, ['get_balance_gas', account], self.GetWallet1(), '07', '05')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger(), 10000000000)

        tx, results, total_ops, engine = TestBuild(out, ['get_balance_neo', account], self.GetWallet1(), '07', '05')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger(), 10000000000)
