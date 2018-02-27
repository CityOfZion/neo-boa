from boa_test.tests.boa_test import BoaTest
from boa.compiler import Compiler

from neo.Prompt.Commands.BuildNRun import TestBuild


class TestContract(BoaTest):

    def test_Concat1(self):
        output = Compiler.instance().load('%s/boa_test/example/ConcatTest.py' % TestContract.dirname).default
        out = output.write()

        tx, results, total_ops, engine = TestBuild(out, [], self.GetWallet1(), '', '07')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetString(), 'helloworld')

    def test_Concat2(self):
        output = Compiler.instance().load('%s/boa_test/example/ConcatTest2.py' % TestContract.dirname).default
        out = output.write()

        tx, results, total_ops, engine = TestBuild(out, ['concat', "['hello','world']"], self.GetWallet1(), '10', '07')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetString(), 'helloworld')

        tx, results, total_ops, engine = TestBuild(out, ['blah', "['hello','world']"], self.GetWallet1(), '10', '07')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBoolean(), False)

        tx, results, total_ops, engine = TestBuild(out, ['concat', "['blah']"], self.GetWallet1(), '10', '07')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBoolean(), False)

        tx, results, total_ops, engine = TestBuild(out, ['concat', "['hello','world','third']"], self.GetWallet1(), '10', '07')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetString(), 'helloworld')

        tx, results, total_ops, engine = TestBuild(out, ['concat', "['1','neo']"], self.GetWallet1(), '10', '07')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetString(), '\x01neo')

        tx, results, total_ops, engine = TestBuild(out, ['concat', "['','neo']"], self.GetWallet1(), '10', '07')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetString(), 'neo')

        # Testinvoke args need to be fixed
#        tx, results, total_ops, engine = TestBuild(out, ['concat',"[bytearray(b'\x01\xa0\x04'),bytearray(b'\x04\x02\x04')]"], self.GetWallet1(), '10','07')
#        self.assertEqual(len(results), 1)
#        self.assertEqual(results[0].GetByteArray(), bytearray(b'\x01\xa0\x04\x04\x02\x04'))

    def test_Take(self):
        output = Compiler.instance().load('%s/boa_test/example/TakeTest.py' % TestContract.dirname).default
        out = output.write()
        tx, results, total_ops, engine = TestBuild(out, [2], self.GetWallet1(), '02', '07')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetString(), 'he')

        tx, results, total_ops, engine = TestBuild(out, [0], self.GetWallet1(), '02', '07')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetString(), '')

        tx, results, total_ops, engine = TestBuild(out, [12], self.GetWallet1(), '02', '07')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetString(), 'helloworld12')

        tx, results, total_ops, engine = TestBuild(out, [40], self.GetWallet1(), '02', '07')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetString(), 'helloworld1234567')

        tx, results, total_ops, engine = TestBuild(out, [-2], self.GetWallet1(), '02', '07')
        self.assertEqual(len(results), 0)
