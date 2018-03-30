from boa.builtins import breakpoint
from boa.interop.Neo.Blockchain import GetBlock
from .demo.AnotherModule import another_module_method


def Main(a):

    ret = False
    j = 12
    if a == 1:
        breakpoint()
        ret = True

    elif a == 2:
        ret = True
        breakpoint()

    elif a == 3:
        breakpoint()
        breakpoint()
        ret = True

    elif a == 4:

        j = 15
        breakpoint()

    elif a == 5:
        ret = another_method(6)

    elif a == 6:
        ret = another_module_method(3)

    elif a == 7:

        block = GetBlock(50424)

        breakpoint()

        ret = False

    return ret


def another_method(q):

    h = q + 43

    m = h / 2

    breakpoint()

    return m
