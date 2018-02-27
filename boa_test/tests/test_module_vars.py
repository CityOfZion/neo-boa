from tests.boa_test import BoaTest
from boa.compiler import Compiler

from neo.Prompt.Commands.BuildNRun import TestBuild


class TestContract(BoaTest):

    def test_M1(self):
        output = Compiler.instance().load('boa_test/example/ModuleVariableTest1.py').default
        out = output.write()

        tx, results, total_ops, engine = TestBuild(out, [], self.GetWallet1(), '', '07')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger(), 8)

    def test_M2(self):
        output = Compiler.instance().load('boa_test/example/ModuleVariableTest.py').default
        out = output.write()

        tx, results, total_ops, engine = TestBuild(out, [], self.GetWallet1(), '', '07')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger(), 1260)

    def test_M3(self):
        output = Compiler.instance().load('boa_test/example/ModuleMethodTest1.py').default
        out = output.write()

        tx, results, total_ops, engine = TestBuild(out, [], self.GetWallet1(), '', '07')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBoolean(), True)

    def test_M4(self):
        output = Compiler.instance().load('boa_test/example/ModuleMethodTest2.py').default
        out = output.write()

        tx, results, total_ops, engine = TestBuild(out, [], self.GetWallet1(), '', '07')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger(), 3003)
