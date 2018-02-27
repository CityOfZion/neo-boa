from boa_test.tests.boa_test import BoaTest
from boa.compiler import Compiler
from neo.Prompt.Commands.BuildNRun import TestBuild


class TestContract(BoaTest):

    def test_list0(self):
        output = Compiler.instance().load('%s/boa_test/example/ArrayTest.py' % TestContract.dirname).default
        out = output.write()
        tx, results, total_ops, engine = TestBuild(out, [0], self.GetWallet1(), '02', '02')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger(), 1)

        tx, results, total_ops, engine = TestBuild(out, [1], self.GetWallet1(), '02', '02')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger(), 6)

        tx, results, total_ops, engine = TestBuild(out, [2], self.GetWallet1(), '02', '02')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger(), 3)

        tx, results, total_ops, engine = TestBuild(out, [4], self.GetWallet1(), '02', '02')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger(), 8)

        tx, results, total_ops, engine = TestBuild(out, [8], self.GetWallet1(), '02', '02')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger(), 9)

    def test_list1(self):
        output = Compiler.instance().load('%s/boa_test/example/ArrayTest1.py' % TestContract.dirname).default
        out = output.write()
        tx, results, total_ops, engine = TestBuild(out, [], self.GetWallet1(), '', '02')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBoolean(), True)

    def test_list2(self):
        output = Compiler.instance().load('%s/boa_test/example/ArrayTest2.py' % TestContract.dirname).default
        out = output.write()
        tx, results, total_ops, engine = TestBuild(out, [], self.GetWallet1(), '', '02')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetByteArray(), bytearray(b'\xa0'))

    def test_list3(self):
        output = Compiler.instance().load('%s/boa_test/example/ArrayTest3.py' % TestContract.dirname).default
        out = output.write()
        tx, results, total_ops, engine = TestBuild(out, [], self.GetWallet1(), '', '02')
        self.assertEqual(len(results), 1)
        res = results[0].GetArray()
        self.assertEqual(len(res), 3)
        self.assertEqual(res[0].GetBigInteger(), 1)

    def test_list4(self):
        output = Compiler.instance().load('%s/boa_test/example/AppendTest.py' % TestContract.dirname).default
        out = output.write()
        tx, results, total_ops, engine = TestBuild(out, [], self.GetWallet1(), '', '02')
        self.assertEqual(len(results), 1)
        res = results[0].GetArray()
        self.assertEqual(len(res), 2)
        self.assertEqual(res[0].GetBigInteger(), 6)

    def test_list5(self):
        output = Compiler.instance().load('%s/boa_test/example/ArrayRemoveTest.py' % TestContract.dirname).default
        out = output.write()
        tx, results, total_ops, engine = TestBuild(out, [], self.GetWallet1(), '', '02')
        self.assertEqual(len(results), 1)
        res = results[0].GetArray()
        self.assertEqual(len(res), 3)
        self.assertEqual(res[0].GetBigInteger(), 16)
        self.assertEqual(res[1].GetBigInteger(), 3)

    def test_list6(self):
        output = Compiler.instance().load('%s/boa_test/example/ArrayReverseTest.py' % TestContract.dirname).default
        out = output.write()
        tx, results, total_ops, engine = TestBuild(out, [], self.GetWallet1(), '', '02')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetString(), 'blah')

    def test_list7(self):
        output = Compiler.instance().load('%s/boa_test/example/ArrayTest4.py' % TestContract.dirname).default
        out = output.write()
        tx, results, total_ops, engine = TestBuild(out, [], self.GetWallet1(), '', '02')
        self.assertEqual(len(results), 1)
        res = results[0].GetArray()
        self.assertEqual(len(res), 3)
        self.assertEqual(res[0].GetBigInteger(), 3)
