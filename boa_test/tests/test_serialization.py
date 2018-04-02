from boa_test.tests.boa_test import BoaTest
from boa.compiler import Compiler
from neo.VM.InteropService import StackItem, Array, ByteArray
from neocore.IO.BinaryReader import BinaryReader
from neo.IO.MemoryStream import StreamManager
from neo.Prompt.Commands.BuildNRun import TestBuild


class TestContract(BoaTest):

    def test_serialization_1(self):
        output = Compiler.instance().load('%s/boa_test/example/demo/SerializationTest.py' % TestContract.dirname).default
        out = output.write()
        tx, results, total_ops, engine = TestBuild(out, [1], self.GetWallet1(), '02', '05')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetByteArray(), bytearray(b'\x80\x05\x00\x01a\x02\x01\x03\x80\x03\x00\x01j\x02\x01\x03\x02\x01\x05\x00\x02jk\x00\x07lmnopqr'))

    def test_serialization_2(self):
        output = Compiler.instance().load('%s/boa_test/example/demo/SerializationTest.py' % TestContract.dirname).default
        out = output.write()
        tx, results, total_ops, engine = TestBuild(out, [2], self.GetWallet1(), '02', '05')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetByteArray(), bytearray(b'\x80\x05\x00\x01a\x02\x01\x03\x80\x03\x00\x01j\x02\x01\x03\x02\x01\x05\x00\x02jk\x00\x07lmnopqr'))

        stream = StreamManager.GetStream(results[0].GetByteArray())
        reader = BinaryReader(stream)
        stack_item = StackItem.DeserializeStackItem(reader)

        self.assertIsInstance(stack_item, Array)
        self.assertEqual(stack_item.Count, 5)
        self.assertEqual(stack_item.GetArray()[-1].GetString(), 'lmnopqr')

    def test_serialization_3(self):
        output = Compiler.instance().load('%s/boa_test/example/demo/SerializationTest.py' % TestContract.dirname).default
        out = output.write()
        tx, results, total_ops, engine = TestBuild(out, [3], self.GetWallet1(), '02', '05')
        self.assertEqual(len(results), 1)
        stack_item = results[0].GetArray()

        self.assertIsInstance(stack_item, list)
        self.assertEqual(len(stack_item), 5)
        self.assertEqual(stack_item[-1].GetString(), 'lmnopqr')

    def test_serialization_4(self):
        output = Compiler.instance().load('%s/boa_test/example/demo/SerializationTest.py' % TestContract.dirname).default
        out = output.write()
        tx, results, total_ops, engine = TestBuild(out, [4], self.GetWallet1(), '02', '05')
        self.assertEqual(len(results), 1)
        stack_item = results[0].GetArray()

        self.assertIsInstance(stack_item, list)
        self.assertEqual(len(stack_item), 3)
        self.assertEqual(stack_item[-1].GetBigInteger(), 5)
