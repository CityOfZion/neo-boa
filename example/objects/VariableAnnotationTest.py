from .stuff.things import Awesome, MoreAwesome


def Main(a):

    b = 10  # type:int

    k = Awesome()  # type:Awesome

    m = what()  # type:MoreAwesome

    j = 'stnahoeu'  # type:str

    q = b'\x00'  # type:bytes

    ba = bytearray(b'\x00\x01')  # type:bytearray

    return m.awesome


def what():

    q = MoreAwesome()

    return q
