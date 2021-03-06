import json
import os

from boa.compiler import Compiler
from boa_test.tests.boa_test import BoaTest


class TestContract(BoaTest):
    def test_abi_methods_success(self):
        path = '%s/boa_test/example/AbiMethods1.py' % TestContract.dirname
        output = Compiler.load(path).default
        json_file = json.loads(output.generate_abi_json('AbiMethods1.avm', 'test'))

        entry_point = json_file['entrypoint']
        self.assertEqual(entry_point, 'main')
        functions = json_file['functions']
        self.assertEqual(len(functions), 2)

        main_function = functions[0]
        main_params = main_function['parameters']
        self.assertEqual(main_function['name'], 'main')
        self.assertEqual(main_function['returntype'], 'Any')
        self.assertEqual(len(main_params), 2)
        self.assertEqual(main_params[0]['name'], 'operation')
        self.assertEqual(main_params[0]['type'], 'String')
        self.assertEqual(main_params[1]['name'], 'args')
        self.assertEqual(main_params[1]['type'], 'Array')

        add_function = functions[1]
        add_params = add_function['parameters']
        self.assertEqual(add_function['name'], 'add')
        self.assertEqual(add_function['returntype'], 'Integer')
        self.assertEqual(len(add_params), 2)
        self.assertEqual(add_params[0]['name'], 'a')
        self.assertEqual(add_params[0]['type'], 'Integer')
        self.assertEqual(add_params[1]['name'], 'b')
        self.assertEqual(add_params[1]['type'], 'Integer')

    def test_abi_script_hash_fail(self):
        path = '%s/boa_test/example/AbiMethods1.py' % TestContract.dirname
        abi_path = path.replace('.py', '.abi.json')
        Compiler.load_and_save(path)

        self.assertTrue(os.path.exists(abi_path))
        with open(abi_path, 'r') as abi_file:
            json_file = json.loads(abi_file.read())

        self.assertIn('hash', json_file)
        script_hash = json_file['hash']
        self.assertNotEqual(script_hash, 'a623cc41d62bf5783acde35fd105cdc4')

    def test_abi_script_hash_success(self):
        path = '%s/boa_test/example/AbiMethods1.py' % TestContract.dirname
        abi_path = path.replace('.py', '.abi.json')
        Compiler.load_and_save(path)

        self.assertTrue(os.path.exists(abi_path))
        with open(abi_path, 'r') as abi_file:
            json_file = json.loads(abi_file.read())

        self.assertIn('hash', json_file)
        script_hash = json_file['hash']
        self.assertEqual(script_hash, '0xd0fce96885b76b14beed1c401af22d438ace50d4')

    def test_abi_methods_only_entry_point(self):
        path = '%s/boa_test/example/AbiMethods2.py' % TestContract.dirname
        output = Compiler.load(path).default
        json_file = json.loads(output.generate_abi_json('AbiMethods2.avm', 'test'))

        entry_point = json_file['entrypoint']
        self.assertEqual(entry_point, 'main')
        functions = json_file['functions']
        self.assertEqual(len(functions), 1)

        main_function = functions[0]
        main_params = main_function['parameters']
        self.assertEqual(main_function['name'], 'main')
        self.assertEqual(main_function['returntype'], 'Any')
        self.assertEqual(len(main_params), 2)
        self.assertEqual(main_params[0]['name'], 'operation')
        self.assertEqual(main_params[0]['type'], 'String')
        self.assertEqual(main_params[1]['name'], 'args')
        self.assertEqual(main_params[1]['type'], 'Array')

    def test_abi_methods_without_entry_point(self):
        path = '%s/boa_test/example/AbiMethods3.py' % TestContract.dirname
        output = Compiler.load(path).default
        self.assertEqual(len(output.abi_methods), 1)
        self.assertEqual(output.abi_entry_point, None)
        self.assertRaises(Exception, output.write)

    def test_abi_methods_two_entry_points(self):
        path = '%s/boa_test/example/AbiMethods4.py' % TestContract.dirname
        self.assertRaises(Exception, Compiler.load, path)

    def test_abi_method_more_types_than_arguments(self):
        path = '%s/boa_test/example/AbiMethods5.py' % TestContract.dirname
        self.assertRaises(Exception, Compiler.load, path)

    def test_abi_method_less_types_than_arguments(self):
        path = '%s/boa_test/example/AbiMethods6.py' % TestContract.dirname
        self.assertRaises(Exception, Compiler.load, path)

    def test_abi_method_without_return_type(self):
        path = '%s/boa_test/example/AbiMethods7.py' % TestContract.dirname
        output = Compiler.load(path).default
        json_file = json.loads(output.generate_abi_json('AbiMethods7.avm', 'test'))

        entry_point = json_file['entrypoint']
        self.assertEqual(entry_point, 'main')
        functions = json_file['functions']
        self.assertEqual(len(functions), 1)

        main_function = functions[0]
        main_params = main_function['parameters']
        self.assertEqual(main_function['name'], 'main')
        self.assertEqual(main_function['returntype'], 'Void')
        self.assertEqual(len(main_params), 2)
        self.assertEqual(main_params[0]['name'], 'operation')
        self.assertEqual(main_params[0]['type'], 'String')
        self.assertEqual(main_params[1]['name'], 'args')
        self.assertEqual(main_params[1]['type'], 'Array')

    def test_abi_method_without_decorator(self):
        path = '%s/boa_test/example/AbiMethods8.py' % TestContract.dirname
        output = Compiler.load(path).default
        json_file = json.loads(output.generate_abi_json('AbiMethods8.avm', 'test'))

        entry_point = json_file['entrypoint']
        self.assertEqual(entry_point, 'method')
        functions = json_file['functions']
        self.assertEqual(len(functions), 0)
