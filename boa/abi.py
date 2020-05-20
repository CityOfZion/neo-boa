# write clear when using as params for @abi_entry_point and @abi_method
ByteArray = 'ByteArray'
Integer = 'Integer'
Boolean = 'Boolean'
String = 'String'
Array = 'Array'
Struct = 'Struct'
Map = 'Map'
Interface = 'Interface'
Any = 'Any'
Void = 'Void'

types = {
    'ByteArray': 'ByteArray',
    'Integer': 'Integer',
    'Boolean': 'Boolean',
    'String': 'String',
    'Array': 'Array',
    'Struct': 'Struct',
    'Map': 'Map',
    'Interface': 'Interface',
    'Any': 'Any',
    'Void': 'Void'
}


def is_abi_type(value):
    return value in types


def abi_method(*args):
    return None


def abi_entry_point(*args):
    return None
