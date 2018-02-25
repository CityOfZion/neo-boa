from unittest import TestCase
from boa.compiler import Compiler
import os


class CompilerTestCase(TestCase):

    TEST_SC_OUTPUT = './example/AddTest1.avm'
    TEST_SC_PATH = './example/AddTest1.py'

    @classmethod
    def setUpClass(cls):
        try:
            os.remove(cls.TEST_SC_OUTPUT)
        except Exception as e:
            pass

    def test_compile_1(self):

        sc = Compiler.load_and_save('./example/AddTest1.py')

        self.assertTrue(os.path.exists(self.TEST_SC_OUTPUT))

    def test_compile_2(self):

        sc = Compiler.load('./example/AddTest1.py')

        default_module = sc.default

        to_s = default_module.to_s()

        output = sc.write()

        self.assertIsInstance(output, bytes)

        self.assertTrue(len(output) > 0)
