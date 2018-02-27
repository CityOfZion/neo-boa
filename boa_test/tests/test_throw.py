from boa_test.tests.boa_test import BoaTest
from boa.compiler import Compiler

from neo.Prompt.Commands.BuildNRun import TestBuild


class TestContract(BoaTest):

    def test_Throw1(self):
        output = Compiler.instance().load('%s/boa_test/example/ThrowTest.py' % TestContract.dirname).default
        out = output.write()
        tx, results, total_ops, engine = TestBuild(out, [1], self.GetWallet1(), '02', '07')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBoolean(), True)

        tx, results, total_ops, engine = TestBuild(out, [4], self.GetWallet1(), '02', '07')
        self.assertEqual(len(results), 0)

    def test_Throw2(self):
        output = Compiler.instance().load('%s/boa_test/example/ThrowIfNotTest.py' % TestContract.dirname).default
        out = output.write()
        tx, results, total_ops, engine = TestBuild(out, [True], self.GetWallet1(), '01', '07')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBoolean(), True)

        tx, results, total_ops, engine = TestBuild(out, [False], self.GetWallet1(), '01', '07')
        self.assertEqual(len(results), 0)
