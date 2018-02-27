import pdb
import binascii
from boa.code import pyop


class appcall():

    script_hash = None
    script_args = None

    method_name = None

    def __init__(self, block):

        arguments = []

        for i, item in enumerate(block):
            if item.opcode == pyop.LOAD_CONST:
                arguments.append(item.arg)
            elif item.opcode == pyop.STORE_NAME:
                self.method_name = item.arg

        self.script_hash = arguments[0]

        self.script_args = arguments

        if type(self.script_hash) is str:
            if len(self.script_hash) != 40:
                raise Exception(
                    "Invalid script hash! length of string must be 40")
        elif type(self.script_hash) in [bytes, bytearray]:
            if len(self.script_hash) != 20:
                raise Exception(
                    "Invalid Script hash, length in bytes must be 20")
        else:
            raise Exception(
                "Invalid script hash type.  must be string, bytes, or bytearray")

    @property
    def script_hash_addr(self):
        """

        :return:
        """

        return appcall.to_script_hash_data(self.script_hash)

    @staticmethod
    def to_script_hash_data(item):
        """

        :return:
        """
        b_array = None
        if type(item) is str:
            bstring = item.encode('utf-8')
            b_array = bytearray(binascii.unhexlify(bstring))
        elif type(item) is bytearray:
            pass
        elif type(item) is bytes:
            b_array = bytearray(item)
        else:
            raise Exception("Invalid script hash")

        b_array.reverse()

        print("Script hash data %s " % b_array)

        return bytes(b_array)
