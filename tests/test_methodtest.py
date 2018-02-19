from tests.boa_test import BoaTest
from boa.compiler import Compiler
from neo.Prompt.Commands.BuildNRun import TestBuild

class TestContract(BoaTest):


    def test_Method1(self):

        output = Compiler.instance().load('example/MethodTest.py').default
        out = output.write()
#        print("out %s " % output.to_s())
        tx, results, total_ops, engine = TestBuild(out, [1,2], self.GetWallet1(), '0202','02')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger(), 7)

        tx, results, total_ops, engine = TestBuild(out, [-3, -100], self.GetWallet1(), '0202','02')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger(), -99)


    def test_Method2(self):

        output = Compiler.instance().load('example/MethodTest2.py').default
        out = output.write()
#        print("out %s " % output.to_s())
        tx, results, total_ops, engine = TestBuild(out, [], self.GetWallet1(), '','02')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger(), 26)

    def test_MethodTest4(self):
        output = Compiler.instance().load('example/MethodTest4.py').default
        out = output.write()
        #        print("out %s " % output.to_s())
        tx, results, total_ops, engine = TestBuild(out, [], self.GetWallet1(), '', '02')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger(), 63)
