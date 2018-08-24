from boa_test.tests.boa_test import BoaTest
from boa.compiler import Compiler
from neo.Settings import settings
from neo.Prompt.Commands.BuildNRun import TestBuild


class TestContract(BoaTest):

    def test_dict1(self):

        output = Compiler.instance().load('%s/boa_test/example/DictTest4.py' % TestContract.dirname).default
        out = output.write()
        tx, results, total_ops, engine = TestBuild(out, [], self.GetWallet1(), '', '02')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger(), 10)

    def test_dict2(self):

        with self.assertRaises(Exception) as ctx:
            Compiler.instance().load('%s/boa_test/example/DictTest5_ShouldNotCompile.py' % TestContract.dirname).default.write()

    def test_dict3(self):

        with self.assertRaises(Exception) as ctx:
            Compiler.instance().load('%s/boa_test/example/DictTest6_ShouldNotCompile.py' % TestContract.dirname).default.write()

    def test_dict_keys1(self):
        output = Compiler.instance().load('%s/boa_test/example/DictTestKeys.py' % TestContract.dirname).default
        out = output.write()
        tx, results, total_ops, engine = TestBuild(out, [], self.GetWallet1(), '', '02')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetByteArray(), bytearray(b'ab\x04mzmcallltrs'))

    def test_dict_values1(self):
        output = Compiler.instance().load('%s/boa_test/example/DictTestValues.py' % TestContract.dirname).default
        out = output.write()
        tx, results, total_ops, engine = TestBuild(out, [], self.GetWallet1(), '', '02')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger(), 55)

    def test_dict_has_key(self):
        output = Compiler.instance().load('%s/boa_test/example/DictTestHasKey.py' % TestContract.dirname).default
        out = output.write()
        tx, results, total_ops, engine = TestBuild(out, [], self.GetWallet1(), '', '02')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger(), 22)
