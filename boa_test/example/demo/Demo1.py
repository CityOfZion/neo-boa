
from boa.builtins import concat


def Main(operation, idx1, idx2):

    print("hello")

    # idx1 = 1
    # idx2 = 3

    mylist = [1, 2, 3, 5, 9, 1000, 32, -1]

    mystr_list = ['ab', 'bc', 'de', 'ef']

    if operation == 'add':

        return mylist[idx1] + mylist[idx2]

    elif operation == 'sub':

        return mylist[idx1] - mylist[idx2]

    elif operation == 'fun':
        # my_method( 4, 6 ) == 10

        return my_method(my_method_2(mylist[idx1]), my_method_3(mylist[idx2]))

#    elif operation == 'concat_fun':

#        return concat(mystr_list[idx1], concat(mystr_list[idx2], concat(mystr_list[idx1])))

    return False


def my_method(a, b):

    return a + b


def my_method_2(c):

    return c * 2


def my_method_3(j):

    return j + 1
