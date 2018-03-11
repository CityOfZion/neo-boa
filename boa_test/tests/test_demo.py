from boa_test.tests.boa_test import BoaTest
from boa.compiler import Compiler

from neo.Prompt.Commands.BuildNRun import TestBuild


class TestContract(BoaTest):

    def test_Demo(self):

        output = Compiler.instance().load('%s/boa_test/example/demo/Demo1.py' % TestContract.dirname).default.write()

        tx, results, total_ops, engine = TestBuild(output, ['add', 1, 3], self.GetWallet1(), '070202', '02')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger(), 7)

        tx, results, total_ops, engine = TestBuild(output, ['add', 2, 3], self.GetWallet1(), '070202', '02')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger(), 8)
