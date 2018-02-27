from boa_test.tests.boa_test import BoaFixtureTest
from boa.compiler import Compiler
from neo.Core.TX.Transaction import Transaction, TransactionOutput, TransactionInput
from neo.Core.TX.TransactionAttribute import TransactionAttribute
from neo.Core.CoinReference import CoinReference
from neo.Prompt.Commands.BuildNRun import TestBuild

NEO = bytearray(b'\x9b|\xff\xda\xa6t\xbe\xae\x0f\x93\x0e\xbe`\x85\xaf\x90\x93\xe5\xfeV\xb3J\\"\x0c\xcd\xcfn\xfc3o\xc5')
GAS = bytearray(b'\xe7-(iy\xeel\xb1\xb7\xe6]\xfd\xdf\xb2\xe3\x84\x10\x0b\x8d\x14\x8ewX\xdeB\xe4\x16\x8bqy,`')


class TestContract(BoaFixtureTest):

    def test_Output(self):

        output = Compiler.instance().load('%s/boa_test/example/blockchain/OutputsTest.py' % TestContract.dirname).default
        out = output.write()

        txid = bytearray(b'\xb4A?l#\xdc@7ki<)\x05\xed\xd5\x9a"\xc3I\x10-\x9f#[\xfc\xf6\xb1$N\\\xdb\xce')

        tx, results, total_ops, engine = TestBuild(out, [txid], self.GetWallet1(), '07', '05')
        self.assertEqual(len(results), 1)
        self.assertEqual(len(results[0].GetArray()), 2)

    def test_TransactionTypes(self):

        output = Compiler.instance().load('%s/boa_test/example/blockchain/TransactionTypeTest.py' % TestContract.dirname).default
        out = output.write()

        tx, results, total_ops, engine = TestBuild(out, ['miner'], self.GetWallet1(), '07', '05')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetByteArray(), b'\x00')

        tx, results, total_ops, engine = TestBuild(out, ['issue'], self.GetWallet1(), '07', '05')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetByteArray(), b'\x01')

        tx, results, total_ops, engine = TestBuild(out, ['claim'], self.GetWallet1(), '07', '05')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetByteArray(), b'\x02')

        tx, results, total_ops, engine = TestBuild(out, ['enrollment'], self.GetWallet1(), '07', '05')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetByteArray(), b'\x20')

        tx, results, total_ops, engine = TestBuild(out, ['voting'], self.GetWallet1(), '07', '05')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetByteArray(), b'\x24')

        tx, results, total_ops, engine = TestBuild(out, ['register'], self.GetWallet1(), '07', '05')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetByteArray(), b'\x40')

        tx, results, total_ops, engine = TestBuild(out, ['contract'], self.GetWallet1(), '07', '05')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetByteArray(), b'\x80')

        tx, results, total_ops, engine = TestBuild(out, ['state'], self.GetWallet1(), '07', '05')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetByteArray(), b'\x90')

        tx, results, total_ops, engine = TestBuild(out, ['agency'], self.GetWallet1(), '07', '05')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetByteArray(), b'\xb0')

        tx, results, total_ops, engine = TestBuild(out, ['publish'], self.GetWallet1(), '07', '05')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetByteArray(), b'\xd0')

        tx, results, total_ops, engine = TestBuild(out, ['invocation'], self.GetWallet1(), '07', '05')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetByteArray(), b'\xd1')

    def test_Transaction(self):

        output = Compiler.instance().load('%s/boa_test/example/blockchain/TransactionTest.py' % TestContract.dirname).default
        out = output.write()

        txid = bytearray(b'\xb4A?l#\xdc@7ki<)\x05\xed\xd5\x9a"\xc3I\x10-\x9f#[\xfc\xf6\xb1$N\\\xdb\xce')

        bad_tx = bytearray(b'\xb4A?l#\xdc@7ki<)\x05\xed\xd5\x9a"\xc3I\x10-\x9f#[\xfc\xf6\xb1$N\\\xdb\xca')

        tx, results, total_ops, engine = TestBuild(out, ['get_hash', bad_tx], self.GetWallet1(), '07', '05')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBoolean(), False)

        tx, results, total_ops, engine = TestBuild(out, ['get_hash', txid], self.GetWallet1(), '07', '05')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetByteArray(), txid)

        tx, results, total_ops, engine = TestBuild(out, ['get_type', txid], self.GetWallet1(), '07', '05')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetByteArray(), bytearray(b'\x80'))

        tx, results, total_ops, engine = TestBuild(out, ['get_attrs', txid], self.GetWallet1(), '07', '05')
        self.assertEqual(len(results), 1)
        res = results[0].GetArray()
        self.assertEqual(len(res), 1)
        self.assertIsInstance(res[0].GetInterface(), TransactionAttribute)

        tx, results, total_ops, engine = TestBuild(out, ['get_inputs', txid], self.GetWallet1(), '07', '05')
        self.assertEqual(len(results), 1)
        res = results[0].GetArray()
        self.assertEqual(len(res), 1)
        self.assertIsInstance(res[0].GetInterface(), CoinReference)

        tx, results, total_ops, engine = TestBuild(out, ['get_outputs', txid], self.GetWallet1(), '07', '05')
        self.assertEqual(len(results), 1)
        res = results[0].GetArray()
        self.assertEqual(len(res), 2)
        self.assertIsInstance(res[0].GetInterface(), TransactionOutput)

        tx, results, total_ops, engine = TestBuild(out, ['get_references', txid], self.GetWallet1(), '07', '05')
        res = results[0].GetArray()
        self.assertEqual(len(res), 1)
        self.assertIsInstance(res[0].GetInterface(), TransactionOutput)

        tx, results, total_ops, engine = TestBuild(out, ['get_unspent', txid], self.GetWallet1(), '07', '05')
        self.assertEqual(len(results), 1)
        res = results[0].GetArray()
        self.assertEqual(len(res), 1)
        self.assertIsInstance(res[0].GetInterface(), TransactionOutput)

        tx, results, total_ops, engine = TestBuild(out, ['get_output_details', txid], self.GetWallet1(), '07', '05')
        self.assertEqual(len(results), 1)
        res = results[0].GetArray()
        self.assertEqual(len(res), 2)

        o1 = res[0].GetArray()
        self.assertEqual(len(o1), 3)
        self.assertEqual(o1[0].GetBigInteger(), 100000000)
        self.assertEqual(o1[1].GetByteArray(), NEO)
        self.assertEqual(o1[2].GetByteArray(), bytearray(b"\xe5\x8eY\x99\xbc\xbf]x\xf5.\xad@eA1\xab\xb9\xee\'\t"))

        tx, results, total_ops, engine = TestBuild(out, ['get_reference_details', txid], self.GetWallet1(), '07', '05')
        self.assertEqual(len(results), 1)
        res = results[0].GetArray()
        self.assertEqual(len(res), 1)

        o1 = res[0].GetArray()
        self.assertEqual(len(o1), 3)
        self.assertEqual(o1[0].GetBigInteger(), 98700000000)
        self.assertEqual(o1[1].GetByteArray(), NEO)
        self.assertEqual(o1[2].GetByteArray(), bytearray(b"\xe5:\'\xd3}\x7fZ1\x87\x00<!\xef\xe3rS\x04\xa7A\x06"))

        tx, results, total_ops, engine = TestBuild(out, ['get_input_details', txid], self.GetWallet1(), '07', '05')
        self.assertEqual(len(results), 1)
        res = results[0].GetArray()
        self.assertEqual(len(res), 2)
        self.assertEqual(res[0].GetByteArray(), bytearray(b'\x02\x06\xcco\x91\x96\x95\xfbU\xc9`\\U\x12q(\xc2\x96\x97\xd7\x91\xaf\x88L&6Ali\xa9D\x88'))
        self.assertEqual(res[1].GetBigInteger(), 1)
