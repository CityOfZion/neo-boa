from boa_test.tests.boa_test import BoaFixtureTest
from boa.compiler import Compiler
from neo.Core.TX.Transaction import Transaction
from neo.Prompt.Commands.BuildNRun import TestBuild


class TestContract(BoaFixtureTest):

    def test_Runtime(self):

        output = Compiler.instance().load('%s/boa_test/example/blockchain/ExecutionEngineTest.py' % TestContract.dirname).default
        out = output.write()

        tx, results, total_ops, engine = TestBuild(out, ['executing_sh'], self.GetWallet1(), '07', '05')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetByteArray(), bytearray(b'"rGz\xda\x8d>\xe4K,Q`_\xcc\x87\xe0\x9f\xd9d\x17'))

        tx, results, total_ops, engine = TestBuild(out, ['calling_sh'], self.GetWallet1(), '07', '05')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetByteArray(), bytearray(b'\xff\x95\xd6\x94\xf9\xf7\xaf\xcd\xf5\xc0\xbfe\xedz\x1c\xb4.\xdd\xa1\xd3'))

        tx, results, total_ops, engine = TestBuild(out, ['entry_sh'], self.GetWallet1(), '07', '05')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetByteArray(), bytearray(b'\xc4\xf0\xf0\x18\xfe\x96e\xf2J\xe7j\xe0\xb0\tW\xc5\x1e.\x13t'))

        tx, results, total_ops, engine = TestBuild(out, ['script_container'], self.GetWallet1(), '07', '05')
        self.assertEqual(len(results), 1)
        self.assertEqual(len(results), 1)
        res = results[0].GetInterface()
        self.assertIsInstance(res, Transaction)
        self.assertEqual(res, tx)
