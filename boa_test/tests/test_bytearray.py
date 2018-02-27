from boa_test.tests.boa_test import BoaTest
from boa.compiler import Compiler

from neo.Prompt.Commands.BuildNRun import TestBuild


class TestContract(BoaTest):

    def test_BA1(self):
        output = Compiler.instance().load('%s/boa_test/example/ByteArrayTest.py' % TestContract.dirname).default
        out = output.write()
        tx, results, total_ops, engine = TestBuild(out, [], self.GetWallet1(), '', '07')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetByteArray(), bytearray(b'\t\x01\x02\xaf\t'))

    def test_BA2(self):
        output = Compiler.instance().load('%s/boa_test/example/ByteArrayTest2.py' % TestContract.dirname).default
        out = output.write()
        tx, results, total_ops, engine = TestBuild(out, [bytearray(b'abcefghi'), bytearray(b'zyxwvutrs')], self.GetWallet1(), '0505', '05')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetByteArray(), bytearray(b'bcefghistaoheustnauzyxwvutrs'))

    def test_BA3(self):
        output = Compiler.instance().load('%s/boa_test/example/ByteArrayTest3.py' % TestContract.dirname).default
        out = output.write()
        tx, results, total_ops, engine = TestBuild(out, [], self.GetWallet1(), '', '05')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetByteArray(), bytearray(b'\x01\x02\xaa\xfe'))
