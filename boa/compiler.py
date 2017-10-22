import os
from boa.code.module import Module


class Compiler():
    """
    The main compiler interface class.

    The following loads a python file, compiles it to the `.avm` format
    and saves it alongside the python file.
    
    .. code-block:: python

        from boa.compiler import Compiler
        Compiler.load_and_save('path/to/your/file.py')

        # return the compiler object for inspection
        compiler = Compiler.load('path/to/your/file.py')

        # retrieve the default module for inpection
        default_module = compiler.default

        # retreive the default/entry method for the smart contract
        entry_method = default_module.main
    """
    
    __instance = None
    
    modules = None

    def __init__(self):
        self.modules = []

    @staticmethod
    def instance():
        """
        Retrieve the current instance of the Compiler object, if it exists,
        or create one.

        :return: the singleton instance of the Compiler object
        """
        
        if not Compiler.__instance:
            Compiler.__instance = Compiler()
        return Compiler.__instance

    @property
    def default(self):
        """
        Retrieve the default or 'entry' module.

        :return: the default `boa.code.Module` object or None upon exception
        """
        
        try:
            return self.modules[0]
        except Exception as e:
            pass
            
        return None

    @staticmethod
    def write_file(data, path):
        """
        Save the output data to the file system at the specified path.

        :param data: a byte string of data to write to disk
        :param path: the path to write the file to
        """
        
        with open(path, 'wb+') as out_file:
            out_file.write(data)
            
        return None

    def write(self):
        """
        Write the default module to a byte string.

        :return: a byte string of the compiled Python program
        """
        
        module = self.default
        out_bytes = bytes(module.write())

        return out_bytes

    @staticmethod
    def load_and_save(path, output_path=None):
        """
        Call `load_and_save` to load a Python file to be compiled to the .avm format and save the result.
        By default, the resultant .avm file is saved along side the source file.

        :param path: The path of the Python file to compile
        :param output_path: Optional path to save the compiled `.avm` file
        :return: Returns the instance of the compiler

        Usage:
        The following returns the compiler object for inspection

        .. code-block:: python

            from boa.compiler import Compiler
        
            Compiler.load_and_save('path/to/your/file.py')
        """

        compiler = Compiler.load(path)
        data = compiler.write()

        if output_path is None:   
            fullpath = os.path.realpath(path)
            path, filename = os.path.split(fullpath)
            newfilename = filename.replace('.py', '.avm')
            output_path = '%s/%s' % (path, newfilename)
        
        Compiler.write_file(data, output_path)

        return data

    @staticmethod
    def load(path):
        """
        Call `load` to load a Python file to be compiled but not to write to .avm

        :param path: the path of the Python file to compile
        :return: The instance of the compiler

        Usage:
        The following returns the compiler object for inspection.

        .. code-block:: python

            from boa.compiler import Compiler
        
            compiler = Compiler.load('path/to/your/file.py')
        """

        Compiler.__instance = None

        compiler = Compiler.instance()

        module = Module(path)
        compiler.modules.append(module)

        return compiler
