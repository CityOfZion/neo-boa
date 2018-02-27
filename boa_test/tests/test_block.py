from boa_test.tests.boa_test import BoaFixtureTest
from boa.compiler import Compiler
from neo.Core.TX.Transaction import Transaction
from neo.Prompt.Commands.BuildNRun import TestBuild


class TestContract(BoaFixtureTest):

    def test_Block(self):
        output = Compiler.instance().load('%s/boa_test/example/blockchain/BlockTest.py' % TestContract.dirname).default
        out = output.write()

        tx, results, total_ops, engine = TestBuild(out, ['get_hash', 1234], self.GetWallet1(), '02', '02')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetByteArray(), bytearray(b'R\xddI\xd3\xb5\x92z\x00C3|\x0fR\x8c\xdb$Q\x1e\x1e\xf0s\x856\xd4Uv/mw\xde\x0f\xa5'))

        tx, results, total_ops, engine = TestBuild(out, ['get_index', 1234], self.GetWallet1(), '02', '02')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger(), 1234)

        tx, results, total_ops, engine = TestBuild(out, ['get_timestamp', 1234], self.GetWallet1(), '02', '02')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger(), 1494424275)

        tx, results, total_ops, engine = TestBuild(out, ['get_index', 1234], self.GetWallet1(), '02', '02')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger(), 1234)

        tx, results, total_ops, engine = TestBuild(out, ['get_prevhash', 1234], self.GetWallet1(), '02', '02')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetByteArray(), bytearray(b'*\xaf\xd3\x12\xb5\x06\xca\xfc\x96\xd9\x1e\x1a",!\xa0\xc7P\x9cC\xab2\x82\xbf\xc3\xa5\xf8\xde\x9bE\x90\xbe'))

        tx, results, total_ops, engine = TestBuild(out, ['get_version', 1234], self.GetWallet1(), '02', '02')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger(), 0)

        tx, results, total_ops, engine = TestBuild(out, ['get_nextconsensus', 1234], self.GetWallet1(), '02', '02')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetByteArray(), bytearray(b'\xf3\x81-\xb9\x82\xf3\xb0\x08\x9a!\xa2x\x98\x8e\xfe\xecj\x02{%'))

        tx, results, total_ops, engine = TestBuild(out, ['get_merkleroot', 1234], self.GetWallet1(), '02', '02')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetByteArray(), bytearray(b'\xa2\x99\xbf-\xbb\xf7&<\n+k9\xe1\xa3\xeb\xdb\xad".7nD\xac\x12v,\xfd\x1c$\x02_\xed'))

        tx, results, total_ops, engine = TestBuild(out, ['get_consensusdata', 1234], self.GetWallet1(), '02', '02')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetByteArray(), bytearray(b'sk\xacH\xec;\x0ev'))

        tx, results, total_ops, engine = TestBuild(out, ['get_transactioncount', 1234], self.GetWallet1(), '02', '02')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger(), 1)

        tx, results, total_ops, engine = TestBuild(out, ['get_transactions', 1234], self.GetWallet1(), '02', '02')
        self.assertEqual(len(results), 1)
        res = results[0].GetArray()
        self.assertEqual(len(res), 1)

        tx, results, total_ops, engine = TestBuild(out, ['get_transaction', 1234], self.GetWallet1(), '02', '02')
        self.assertEqual(len(results), 1)
        res = results[0].GetInterface()
        self.assertIsInstance(res, Transaction)
