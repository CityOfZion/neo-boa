from boa_test.tests.boa_test import BoaTest
from boa.compiler import Compiler

from neo.Prompt.Commands.BuildNRun import TestBuild


class TestContract(BoaTest):

    def test_aWhile1(self):
        output = Compiler.instance().load('%s/boa_test/example/WhileTest1.py' % TestContract.dirname).default
        out = output.write()
        tx, results, total_ops, engine = TestBuild(out, [], self.GetWallet1(), '', '07')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger(), 6)

    def test_aWhile2(self):
        output = Compiler.instance().load('%s/boa_test/example/WhileTest2.py' % TestContract.dirname).default
        out = output.write()
        tx, results, total_ops, engine = TestBuild(out, [], self.GetWallet1(), '', '07')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger(), 6)

    def test_aWhile3(self):
        output = Compiler.instance().load('%s/boa_test/example/WhileTest.py' % TestContract.dirname).default
        out = output.write()
        tx, results, total_ops, engine = TestBuild(out, [], self.GetWallet1(), '', '07')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger(), 24)

    def test_Iter1(self):
        output = Compiler.instance().load('%s/boa_test/example/IterTest.py' % TestContract.dirname).default
        out = output.write()
        tx, results, total_ops, engine = TestBuild(out, [], self.GetWallet1(), '', '07')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger(), 18)

    def test_Iter2(self):
        output = Compiler.instance().load('%s/boa_test/example/IterTest2.py' % TestContract.dirname).default
        out = output.write()
        tx, results, total_ops, engine = TestBuild(out, [], self.GetWallet1(), '', '07')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger(), 8)

    def test_Iter3(self):
        output = Compiler.instance().load('%s/boa_test/example/IterTest3.py' % TestContract.dirname).default
        out = output.write()
        tx, results, total_ops, engine = TestBuild(out, [], self.GetWallet1(), '', '07')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger(), 7)

    def test_Iter4(self):
        output = Compiler.instance().load('%s/boa_test/example/IterTest4.py' % TestContract.dirname).default
        out = output.write()
        tx, results, total_ops, engine = TestBuild(out, [], self.GetWallet1(), '', '07')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetByteArray(), bytearray(b'abcdabcdabcd\x0c'))

    def test_Iter5(self):
        output = Compiler.instance().load('%s/boa_test/example/IterTest5.py' % TestContract.dirname).default
        out = output.write()
        tx, results, total_ops, engine = TestBuild(out, [], self.GetWallet1(), '', '07')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger(), 51)

    def test_Range1(self):
        output = Compiler.instance().load('%s/boa_test/example/RangeTest.py' % TestContract.dirname).default
        out = output.write()
        tx, results, total_ops, engine = TestBuild(out, [], self.GetWallet1(), '', '07')
        self.assertEqual(len(results), 1)
        res = results[0].GetArray()
        self.assertEqual(len(res), 20)

    def test_Range2(self):
        output = Compiler.instance().load('%s/boa_test/example/IterTest6.py' % TestContract.dirname).default
        out = output.write()
        tx, results, total_ops, engine = TestBuild(out, [], self.GetWallet1(), '', '07')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger(), 10)

    def test_Range3(self):
        output = Compiler.instance().load('%s/boa_test/example/IterTest7.py' % TestContract.dirname).default
        out = output.write()
        tx, results, total_ops, engine = TestBuild(out, [], self.GetWallet1(), '', '07')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger(), 12)

    def test_Range4(self):
        output = Compiler.instance().load('%s/boa_test/example/IterTest8.py' % TestContract.dirname).default
        out = output.write()
        tx, results, total_ops, engine = TestBuild(out, [], self.GetWallet1(), '', '07')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger(), 6)
