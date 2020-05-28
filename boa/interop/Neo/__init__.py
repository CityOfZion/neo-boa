import hashlib


def to_script_hash(byte_array) -> bytes:
    """
    Converts a data to a script hash.

    :param byte_array: data to hash.
    :type byte_array: bytearray or bytes

    :return: the script hash of the data
    :rtype: bytes
    """
    intermed = hashlib.sha256(byte_array).digest()
    return hashlib.new('ripemd160', intermed).digest()


def to_hex_str(data_bytes: bytes) -> str:
    """
    Converts bytes into its string hex representation.

    :param data_bytes: data to represent as hex.
    :type data_bytes: bytearray or bytes

    :return: the hex representation of the data
    :rtype: str
    """
    if isinstance(data_bytes, bytes):
        data_bytes = bytearray(data_bytes)
    data_bytes.reverse()
    return '0x' + data_bytes.hex()
