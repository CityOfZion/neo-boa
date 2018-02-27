from boa_test.tests.boa_test import BoaTest
from boa.compiler import Compiler

from neo.Prompt.Commands.BuildNRun import TestBuild


class TestContract(BoaTest):

    def test_CompareTest0(self):

        output = Compiler.instance().load('%s/boa_test/example/CompareTest0.py' % TestContract.dirname).default
        out = output.write()

        tx, results, total_ops, engine = TestBuild(out, [2, 4], self.GetWallet1(), '0202', '02')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger(), 2)

        tx, results, total_ops, engine = TestBuild(out, [4, 2], self.GetWallet1(), '0202', '02')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger(), 3)

        tx, results, total_ops, engine = TestBuild(out, [2, 2], self.GetWallet1(), '0202', '02')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger(), 2)

        tx, results, total_ops, engine = TestBuild(out, ['b', 'a'], self.GetWallet1(), '0202', '02')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger(), 3)

        tx, results, total_ops, engine = TestBuild(out, ['a', 'b'], self.GetWallet1(), '0202', '02')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger(), 2)

    def test_CompareTest1(self):

        output = Compiler.instance().load('%s/boa_test/example/CompareTest1.py' % TestContract.dirname).default
        out = output.write()

        tx, results, total_ops, engine = TestBuild(out, [1, 2, 3, 4], self.GetWallet1(), '02020202', '02')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger(), 11)

        tx, results, total_ops, engine = TestBuild(out, [1, 2, 4, 3], self.GetWallet1(), '02020202', '02')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger(), 1)

        tx, results, total_ops, engine = TestBuild(out, [1, 4, 3, 5], self.GetWallet1(), '02020202', '02')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger(), 22)

        tx, results, total_ops, engine = TestBuild(out, [4, 1, 5, 3], self.GetWallet1(), '02020202', '02')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger(), 3)

        tx, results, total_ops, engine = TestBuild(out, [9, 1, 3, 5], self.GetWallet1(), '02020202', '02')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger(), 10)

        tx, results, total_ops, engine = TestBuild(out, [9, 5, 3, 5], self.GetWallet1(), '02020202', '02')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger(), 8)

    def test_CompareTest2(self):

        output = Compiler.instance().load('%s/boa_test/example/CompareTest2.py' % TestContract.dirname).default
        out = output.write()

        tx, results, total_ops, engine = TestBuild(out, [2, 2], self.GetWallet1(), '0202', '01')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBoolean(), True)

        tx, results, total_ops, engine = TestBuild(out, [2, 3], self.GetWallet1(), '0202', '01')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBoolean(), False)
