from boa_test.tests.boa_test import BoaTest
from boa.compiler import Compiler

from neo.Prompt.Commands.BuildNRun import TestBuild


class TestContract(BoaTest):

    def test_compare_in(self):

        output = Compiler.instance().load('%s/boa_test/example/CompareInTest.py' % TestContract.dirname).default
        out = output.write()

        tx, results, total_ops, engine = TestBuild(out, [1], self.GetWallet1(), '', '01')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBoolean(), True)

        tx, results, total_ops, engine = TestBuild(out, [2], self.GetWallet1(), '', '01')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBoolean(), False)

        tx, results, total_ops, engine = TestBuild(out, [3], self.GetWallet1(), '', '01')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBoolean(), True)

        tx, results, total_ops, engine = TestBuild(out, [4], self.GetWallet1(), '', '01')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBoolean(), False)

        tx, results, total_ops, engine = TestBuild(out, [5], self.GetWallet1(), '', '01')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBoolean(), True)

        tx, results, total_ops, engine = TestBuild(out, [6], self.GetWallet1(), '', '01')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBoolean(), True)

        tx, results, total_ops, engine = TestBuild(out, [7], self.GetWallet1(), '', '01')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBoolean(), True)

        tx, results, total_ops, engine = TestBuild(out, [8], self.GetWallet1(), '', '01')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBoolean(), False)

        tx, results, total_ops, engine = TestBuild(out, [9], self.GetWallet1(), '', '01')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBoolean(), True)
