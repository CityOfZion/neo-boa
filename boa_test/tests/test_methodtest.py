from boa_test.tests.boa_test import BoaTest
from boa.compiler import Compiler
from neo.Prompt.Commands.BuildNRun import TestBuild


class TestContract(BoaTest):

    def test_Method1(self):
        output = Compiler.instance().load('%s/boa_test/example/MethodTest.py' % TestContract.dirname).default
        out = output.write()
        tx, results, total_ops, engine = TestBuild(out, [1, 2], self.GetWallet1(), '0202', '02')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger(), 7)

        tx, results, total_ops, engine = TestBuild(out, [-3, -100], self.GetWallet1(), '0202', '02')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger(), -99)

    def test_Method2(self):
        output = Compiler.instance().load('%s/boa_test/example/MethodTest2.py' % TestContract.dirname).default
        out = output.write()
        tx, results, total_ops, engine = TestBuild(out, [], self.GetWallet1(), '', '02')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger(), 26)

    def test_MethodTest3(self):
        output = Compiler.instance().load('%s/boa_test/example/MethodTest3.py' % TestContract.dirname).default
        out = output.write()
        tx, results, total_ops, engine = TestBuild(out, [], self.GetWallet1(), '', '02')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger(), 13)

    def test_MethodTest4(self):
        output = Compiler.instance().load('%s/boa_test/example/MethodTest4.py' % TestContract.dirname).default
        out = output.write()
        tx, results, total_ops, engine = TestBuild(out, [], self.GetWallet1(), '', '02')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger(), 63)

    def test_MethodTest5(self):
        output = Compiler.instance().load('%s/boa_test/example/MethodTest5.py' % TestContract.dirname).default
        out = output.write()
        tx, results, total_ops, engine = TestBuild(out, [], self.GetWallet1(), '', '02')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger(), 15)

    def test_MethodTest6(self):
        output = Compiler.instance().load('%s/boa_test/example/Fibonacci.py' % TestContract.dirname).default
        out = output.write()

        tx, results, total_ops, engine = TestBuild(out, [4], self.GetWallet1(), '02', '02')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger(), 3)

        tx, results, total_ops, engine = TestBuild(out, [5], self.GetWallet1(), '02', '02')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger(), 5)

        tx, results, total_ops, engine = TestBuild(out, [6], self.GetWallet1(), '02', '02')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger(), 8)

        tx, results, total_ops, engine = TestBuild(out, [7], self.GetWallet1(), '02', '02')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger(), 13)

        tx, results, total_ops, engine = TestBuild(out, [11], self.GetWallet1(), '02', '02')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger(), 89)
