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
        self.assertEqual(results[0].GetByteArray(), bytearray(b'\x82\x13\x19\xd7\xfc\x87\xec\xa5\xae\x04\x91\xf60E\xd5\xac\x9a\x07\xe2\xb1'))

        tx, results, total_ops, engine = TestBuild(out, ['calling_sh'], self.GetWallet1(), '07', '05')
        self.assertEqual(len(results), 1)
        print("results: %s " % results[0].GetByteArray())
        self.assertEqual(results[0].GetByteArray(), bytearray(b'\xb6\xa9\xdf\xfe\x85o\xdb<\x04\x7f\xacW\xc6\xc1)\xdb\xc5|\x12\xaa'))

        tx, results, total_ops, engine = TestBuild(out, ['entry_sh'], self.GetWallet1(), '07', '05')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetByteArray(), bytearray(b'2\xdez&\xc4\xc2>\xcbQ0\xa3cJ\x8c\xbdjd\xe9\x8d\xed'))

        tx, results, total_ops, engine = TestBuild(out, ['script_container'], self.GetWallet1(), '07', '05')
        self.assertEqual(len(results), 1)
        self.assertEqual(len(results), 1)
        res = results[0].GetInterface()
        self.assertIsInstance(res, Transaction)
        self.assertEqual(res, tx)
