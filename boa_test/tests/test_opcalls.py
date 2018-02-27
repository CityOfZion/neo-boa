from boa_test.tests.boa_test import BoaTest
from boa.compiler import Compiler

from neo.Prompt.Commands.BuildNRun import TestBuild


class TestContract(BoaTest):

    def test_opcalls(self):

        output = Compiler.instance().load('%s/boa_test/example/OpCallTest.py' % TestContract.dirname).default
        out = output.write()

        tx, results, total_ops, engine = TestBuild(out, ['omin', 4, 4], self.GetWallet1(), '', '07')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger(), 4)

        tx, results, total_ops, engine = TestBuild(out, ['omin', -4, 4], self.GetWallet1(), '', '07')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger(), -4)

        tx, results, total_ops, engine = TestBuild(out, ['omin', 16, 0], self.GetWallet1(), '', '07')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger(), 0)

        tx, results, total_ops, engine = TestBuild(out, ['omax', 4, 4], self.GetWallet1(), '', '07')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger(), 4)

        tx, results, total_ops, engine = TestBuild(out, ['omax', -4, 4], self.GetWallet1(), '', '07')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger(), 4)

        tx, results, total_ops, engine = TestBuild(out, ['omax', 16, 0], self.GetWallet1(), '', '07')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger(), 16)

        tx, results, total_ops, engine = TestBuild(out, ['oabs', 0, 4], self.GetWallet1(), '', '07')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger(), 0)

        tx, results, total_ops, engine = TestBuild(out, ['oabs', -4, 4], self.GetWallet1(), '', '07')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger(), 4)

        tx, results, total_ops, engine = TestBuild(out, ['sha1', 'abc', 4], self.GetWallet1(), '', '07')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetByteArray(), bytearray(b'\xa9\x99>6G\x06\x81j\xba>%qxP\xc2l\x9c\xd0\xd8\x9d'))

        tx, results, total_ops, engine = TestBuild(out, ['sha256', 'abc', 4], self.GetWallet1(), '', '07')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetByteArray(), bytearray(b'\xbax\x16\xbf\x8f\x01\xcf\xeaAA@\xde]\xae"#\xb0\x03a\xa3\x96\x17z\x9c\xb4\x10\xffa\xf2\x00\x15\xad'))

        tx, results, total_ops, engine = TestBuild(out, ['hash160', 'abc', 4], self.GetWallet1(), '', '07')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetByteArray(), bytearray(b'\xbb\x1b\xe9\x8c\x14$D\xd7\xa5j\xa3\x98\x1c9B\xa9x\xe4\xdc3'))

        tx, results, total_ops, engine = TestBuild(out, ['hash256', 'abc', 4], self.GetWallet1(), '', '07')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetByteArray(), bytearray(b'O\x8bB\xc2-\xd3r\x9bQ\x9b\xa6\xf6\x8d-\xa7\xcc[-`m\x05\xda\xedZ\xd5\x12\x8c\xc0>lcX'))
