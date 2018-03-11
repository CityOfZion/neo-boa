from boa_test.tests.boa_test import BoaTest
from boa.compiler import Compiler

from neo.Prompt.Commands.BuildNRun import TestBuild

from neo.Settings import settings


class TestContract(BoaTest):

    def test_ManyElif(self):

        output = Compiler.instance().load('%s/boa_test/example/TestManyElif.py' % TestContract.dirname).default
        out = output.write()

        tx, results, total_ops, engine = TestBuild(out, [1], self.GetWallet1(), '02', '02')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger(), 2)

        tx, results, total_ops, engine = TestBuild(out, [3], self.GetWallet1(), '02', '02')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger(), 4)

        tx, results, total_ops, engine = TestBuild(out, [16], self.GetWallet1(), '02', '02')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger(), 17)

        tx, results, total_ops, engine = TestBuild(out, [22], self.GetWallet1(), '02', '02')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger(), -1)
