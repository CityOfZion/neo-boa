from tests.boa_test import BoaTest
from boa.compiler import Compiler

from neo.Prompt.Commands.BuildNRun import TestBuild


class TestContract(BoaTest):


    def test_Slice1(self):
        output = Compiler.instance().load('example/SliceTest.py').default
        out = output.write()
        tx, results, total_ops, engine = TestBuild(out, [], self.GetWallet1(), '','07')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetByteArray(), bytearray(b'\x01\x02\x03\x04'))


    def test_Slice2(self):
        output = Compiler.instance().load('example/SliceTest2.py').default
        out = output.write()
        tx, results, total_ops, engine = TestBuild(out, [], self.GetWallet1(), '','07')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetByteArray(), bytearray(b'\x02\x03\x04\x02\x03\x04\x05\x06\x01\x02\x03\x04\x03\x04'))

