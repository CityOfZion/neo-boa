from tests.boa_test import BoaTest
from boa.compiler import Compiler

from neo.Prompt.Commands.BuildNRun import TestBuild


class TestContract(BoaTest):
    """
    def test_aWhile1(self):
        output = Compiler.instance().load('example/WhileTest1.py').default
        out = output.write()
        tx, results, total_ops, engine = TestBuild(out, [], self.GetWallet1(), '','07')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger(), 6)

    def test_aWhile2(self):
        output = Compiler.instance().load('example/WhileTest2.py').default
        out = output.write()
        tx, results, total_ops, engine = TestBuild(out, [], self.GetWallet1(), '', '07')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger(), 6)

    def test_aWhile3(self):
        output = Compiler.instance().load('example/WhileTest.py').default
        out = output.write()
        tx, results, total_ops, engine = TestBuild(out, [], self.GetWallet1(), '', '07')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger(), 34)
    def test_Iter1(self):
        output = Compiler.instance().load('example/IterTest.py').default
        out = output.write()
        print(output.to_s())
        tx, results, total_ops, engine = TestBuild(out, [], self.GetWallet1(), '','07')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger(),18)


    def test_Iter2(self):
        output = Compiler.instance().load('example/IterTest2.py').default
        out = output.write()
        print(output.to_s())
        tx, results, total_ops, engine = TestBuild(out, [], self.GetWallet1(), '','07')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger(),8)
    """
    def test_Iter3(self):
        output = Compiler.instance().load('example/IterTest3.py').default
        out = output.write()
        print(output.to_s())
        tx, results, total_ops, engine = TestBuild(out, [], self.GetWallet1(), '','07')
        self.assertEqual(len(results), 1)
#        self.assertEqual(results[0].GetBigInteger(),18)
        print('results %s ' % results)

