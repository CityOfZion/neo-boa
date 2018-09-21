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
        self.assertEqual(results[0].GetByteArray(), bytearray(b'\xd6\xa7Rf\xed\xba\x82?\xb4\xd0\xa5\xfc\xbf\xed\xf8\xb7\xf2\xea\xf5@\xad\xa8\xd8\xa2\xb8\xf5\xd5\xd8\xfe\x8d\xc4\xe1'))

        tx, results, total_ops, engine = TestBuild(out, ['get_index', 1234], self.GetWallet1(), '02', '02')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger(), 1234)

        tx, results, total_ops, engine = TestBuild(out, ['get_timestamp', 1234], self.GetWallet1(), '02', '02')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger(), 1529948750)

        tx, results, total_ops, engine = TestBuild(out, ['get_index', 1234], self.GetWallet1(), '02', '02')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger(), 1234)

        tx, results, total_ops, engine = TestBuild(out, ['get_prevhash', 1234], self.GetWallet1(), '02', '02')
        self.assertEqual(len(results), 1)

        self.assertEqual(results[0].GetByteArray(), bytearray(b'<\xc4\xe9\x1a\xfe3\xabjo\xff\xfc_\xab=\x14\xa6?%\xbc\x0e$G\xa3\xdaVh\xa1\xddT#\xdcF'))

        tx, results, total_ops, engine = TestBuild(out, ['get_version', 1234], self.GetWallet1(), '02', '02')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger(), 0)

        tx, results, total_ops, engine = TestBuild(out, ['get_nextconsensus', 1234], self.GetWallet1(), '02', '02')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetByteArray(), bytearray(b'\xbeH\xd3\xa3\xf5\xd1\x00\x13\xab\x9f\xfe\xe4\x89p`xqO\x1e\xa2'))

        tx, results, total_ops, engine = TestBuild(out, ['get_merkleroot', 1234], self.GetWallet1(), '02', '02')
        self.assertEqual(len(results), 1)

        self.assertEqual(results[0].GetByteArray(), bytearray(b'\xe4FR\xf2U-\xf9\x12\x9c\x15F\x13n\xb5\xc8\xa4z\xac\xb0\xfbK\x1f\xbc\x16*\x14\xd8\xc1\xb8c\xe7\xab'))

        tx, results, total_ops, engine = TestBuild(out, ['get_consensusdata', 1234], self.GetWallet1(), '02', '02')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetByteArray(), bytearray(b'$\xbf=\xdb_Qib'))

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
