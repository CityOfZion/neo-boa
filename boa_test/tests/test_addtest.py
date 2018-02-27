from boa_test.tests.boa_test import BoaTest
from boa.compiler import Compiler

from neo.Prompt.Commands.BuildNRun import TestBuild


class TestContract(BoaTest):

    def test_AddTest(self):

        output = Compiler.instance().load('%s/boa_test/example/AddTest.py' % TestContract.dirname).default.write()

        tx, results, total_ops, engine = TestBuild(output, [2], self.GetWallet1(), '02', '02')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger(), 4)

        tx, results, total_ops, engine = TestBuild(output, [23234], self.GetWallet1(), '02', '02')
        self.assertEqual(results[0].GetBigInteger(), 23236)

        tx, results, total_ops, engine = TestBuild(output, [0], self.GetWallet1(), '02', '02')
        self.assertEqual(results[0].GetBigInteger(), 2)

        tx, results, total_ops, engine = TestBuild(output, [-112], self.GetWallet1(), '02', '02')
        self.assertEqual(results[0].GetBigInteger(), -110)

    def test_AddTest1(self):

        output = Compiler.instance().load('%s/boa_test/example/AddTest1.py' % TestContract.dirname).default.write()

        tx, results, total_ops, engine = TestBuild(output, [1, 2, 3, 4], self.GetWallet1(), '02020202', '02')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger(), 9)

        tx, results, total_ops, engine = TestBuild(output, [0, 0, 0, 2], self.GetWallet1(), '02020202', '02')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger(), 2)

        tx, results, total_ops, engine = TestBuild(output, [-2, 3, -6, 2], self.GetWallet1(), '02020202', '02')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger(), -2)

    def test_AddTest2(self):

        output = Compiler.instance().load('%s/boa_test/example/AddTest2.py' % TestContract.dirname).default.write()

        tx, results, total_ops, engine = TestBuild(output, [], self.GetWallet1(), '', '02')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger(), 3)

    def test_AddTest4(self):

        output = Compiler.instance().load('%s/boa_test/example/AddTest4.py' % TestContract.dirname).default.write()

        tx, results, total_ops, engine = TestBuild(output, [1, 2, 3, 4], self.GetWallet1(), '', '02')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger(), -9)

    def test_AddVoid(self):

        output = Compiler.instance().load('%s/boa_test/example/AddTestVoid.py' % TestContract.dirname).default
        out = output.write()

        tx, results, total_ops, engine = TestBuild(out, [3], self.GetWallet1(), '02', 'ff')
        # this should I guess return nothing
        # for now it returns an empty byte array
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetByteArray(), bytearray(b''))
