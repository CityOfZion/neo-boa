from tests.boa_test import BoaFixtureTest
from boa.compiler import Compiler
from neo.Core.TX.Transaction import Transaction
from neo.Prompt.Commands.BuildNRun import TestBuild


class TestContract(BoaFixtureTest):


    def test_Runtime(self):

        output = Compiler.instance().load('example/blockchain/ExecutionEngineTest.py').default
        out = output.write()

        tx, results, total_ops, engine = TestBuild(out, ['executing_sh'], self.GetWallet1(), '07','05')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetByteArray(), bytearray(b'\xfe\x1b\xd5\x18\xac\xfe3\x90\x83\xc0T\xcf\x11e\xf8q[C8"'))

        tx, results, total_ops, engine = TestBuild(out, ['calling_sh'], self.GetWallet1(), '07','05')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetByteArray(), bytearray(b'\xc6/b\x07\x0e\xf9\x1b\\N\xa8\x14fKU\x82n\xbb)\x8e\x11'))

        tx, results, total_ops, engine = TestBuild(out, ['entry_sh'], self.GetWallet1(), '07','05')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetByteArray(), bytearray(b'\xf0\x82[\n\xbe\xc0\x06\xb3\x83\xfc\x1d\x82\x82/A\x15\xb1\x17p\xad'))

        tx, results, total_ops, engine = TestBuild(out, ['script_container'], self.GetWallet1(), '07','05')
        self.assertEqual(len(results), 1)
        self.assertEqual(len(results), 1)
        res = results[0].GetInterface()
        self.assertIsInstance(res, Transaction)
        self.assertEqual(res, tx)