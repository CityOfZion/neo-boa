from boa_test.tests.boa_test import BoaTest
from boa.compiler import Compiler

from neo.Prompt.Commands.BuildNRun import TestBuild


class TestContract(BoaTest):

    def test_binops(self):
        output = Compiler.instance().load('%s/boa_test/example/BinopTest.py' % TestContract.dirname).default
        out = output.write()

        tx, results, total_ops, engine = TestBuild(out, ['&', 4, 4], self.GetWallet1(), '', '07')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger(), 4)

        tx, results, total_ops, engine = TestBuild(out, ['|', 4, 3], self.GetWallet1(), '', '07')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger(), 7)

        tx, results, total_ops, engine = TestBuild(out, ['|', 4, 8], self.GetWallet1(), '', '07')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger(), 12)

        tx, results, total_ops, engine = TestBuild(out, ['^', 4, 4], self.GetWallet1(), '', '07')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger(), 0)

        tx, results, total_ops, engine = TestBuild(out, ['^', 4, 2], self.GetWallet1(), '', '07')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger(), 6)

        tx, results, total_ops, engine = TestBuild(out, ['>>', 16, 2], self.GetWallet1(), '', '07')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger(), 4)

        tx, results, total_ops, engine = TestBuild(out, ['>>', 16, 0], self.GetWallet1(), '', '07')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger(), 16)

        tx, results, total_ops, engine = TestBuild(out, ['>>', 11, 1], self.GetWallet1(), '', '07')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger(), 5)

        tx, results, total_ops, engine = TestBuild(out, ['<<', 16, 2], self.GetWallet1(), '', '07')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger(), 64)

        tx, results, total_ops, engine = TestBuild(out, ['<<', 16, -2], self.GetWallet1(), '', '07')
        self.assertEqual(len(results), 0)

        tx, results, total_ops, engine = TestBuild(out, ['<<', 4, 5], self.GetWallet1(), '', '07')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger(), 128)

        tx, results, total_ops, engine = TestBuild(out, ['%', 16, 2], self.GetWallet1(), '', '07')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger(), 0)

        tx, results, total_ops, engine = TestBuild(out, ['%', 16, 11], self.GetWallet1(), '', '07')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger(), 5)

        tx, results, total_ops, engine = TestBuild(out, ['//', 16, 2], self.GetWallet1(), '', '07')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger(), 8)

        tx, results, total_ops, engine = TestBuild(out, ['//', 16, 7], self.GetWallet1(), '', '07')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger(), 2)

        tx, results, total_ops, engine = TestBuild(out, ['/', 16, 7], self.GetWallet1(), '', '07')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger(), 2)

        tx, results, total_ops, engine = TestBuild(out, ['~', 16, 0], self.GetWallet1(), '', '07')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger(), -17)

        tx, results, total_ops, engine = TestBuild(out, ['~', -3, 0], self.GetWallet1(), '', '07')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger(), 2)
