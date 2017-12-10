from unittest import TestCase
import os
import glob
from boa.compiler import Compiler


class TestCompileExamples(TestCase):

    basic_items_to_test = []

    blockchain_items_to_test = []

    object_items_to_test = []

    bug_items_to_test = []

    @classmethod
    def setUpClass(cls):

        module_path = 'boa/tests/src'
        py_test = '%s/*.py' % module_path

        test_glob = glob.glob(py_test)

        cls.items_to_test = [item for item in test_glob if '__init__' not in item]
        cls.items_to_test.sort()

        module_path = 'boa/tests/src/blockchain'
        py_test = '%s/*.py' % module_path

        test_glob = glob.glob(py_test)

        cls.blockchain_items_to_test = [item for item in test_glob if '__init__' not in item]
        cls.basic_items_to_test.sort()

        module_path = 'boa/tests/src/objects'
        py_test = '%s/*.py' % module_path

        test_glob = glob.glob(py_test)

        cls.object_items_to_test = [item for item in test_glob if '__init__' not in item]
        cls.object_items_to_test.sort()

        module_path = 'boa/tests/src/bugs'
        py_test = '%s/*.py' % module_path

        test_glob = glob.glob(py_test)

        cls.bug_items_to_test = [item for item in test_glob if '__init__' not in item]
        cls.bug_items_to_test.sort()


    def test_a_single_compile(self):

        # just test a single compilation to see how things are going
        first_item = self.items_to_test[0]

        result = Compiler.load_and_save(first_item)

        self.assertIsNotNone(result)
        self.assertIsInstance(result, bytes)

        # this is the output path
        output = first_item.replace('.py', '.avm')

        # check to make sure it was saved correctly
        self.assertTrue(os.path.isfile(output))

        os.remove(output)

    def test_all_basic_items(self):

        for item in self.items_to_test:
            self._testitem(item)

    def test_blockchain_items(self):

        for item in self.blockchain_items_to_test:
            self._testitem(item)

    def test_object_items(self):

        for item in self.object_items_to_test:
            self._testitem(item)

    def test_bug_items(self):
        for item in self.bug_items_to_test:
            self._testitem(item)

    def _testitem(self, item):

        result = Compiler.load_and_save(item)

        self.assertIsNotNone(result)
        self.assertIsInstance(result, bytes)

        # this is the output path
        output = item.replace('.py', '.avm')

        # check to make sure it was saved correctly
        self.assertTrue(os.path.isfile(output))

        os.remove(output)
