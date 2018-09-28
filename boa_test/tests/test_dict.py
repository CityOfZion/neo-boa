from boa_test.tests.boa_test import BoaTest
from boa.compiler import Compiler
from neo.Settings import settings
from neo.Prompt.Commands.BuildNRun import TestBuild


class TestContract(BoaTest):

    def test_dict1(self):

        output = Compiler.instance().load('%s/boa_test/example/DictTest1.py' % TestContract.dirname).default
        out = output.write()

        tx, results, total_ops, engine = TestBuild(out, [], self.GetWallet1(), '', '02')
        self.assertEqual(len(results), 1)
        self.assertIsInstance(results[0].GetMap(), dict)
        self.assertEqual(results[0].GetBoolean(), True)

    def test_dict2(self):

        output = Compiler.instance().load('%s/boa_test/example/DictTest2.py' % TestContract.dirname).default
        out = output.write()

        tx, results, total_ops, engine = TestBuild(out, [], self.GetWallet1(), '', '02')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger(), 7)

    def test_dict3(self):

        output = Compiler.instance().load('%s/boa_test/example/DictTest3.py' % TestContract.dirname).default
        out = output.write()
        string_ouput = output.to_s()
        self.assertGreater(len(string_ouput), 0)

        tx, results, total_ops, engine = TestBuild(out, [], self.GetWallet1(), '', '02')
        self.assertEqual(len(results), 1)
        self.assertIsInstance(results[0].GetMap(), dict)
