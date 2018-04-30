
def Main(operation):

    mylist = [1, 4, 10]

    q = b'\xab'

    myDict = {
        'a': 1,
        'b': 34,
        'c': 'abc',
        q: '123'
    }

    if operation == 1:

        return 'a' in myDict

    elif operation == 2:

        return 3 in myDict

    elif operation == 3:

        # this should return true
        # the neo-vm uses 'HAS_KEY' op for lists
        # which only checks the length of the array :(
        # it doesn't test whether the array
        # contains the value
        return 2 in mylist

    elif operation == 4:
        # this should return false
        # even though 10 is in the list
        # because the list isn't 10 items long
        return 10 in mylist

    elif operation == 5:

        myDict['h'] = 3

        return 'h' in myDict

    elif operation == 6:

        mylist.append(8)

        return 3 in mylist

    elif operation == 7:

        myDict[7] = 'a'

        return 7 in myDict

    elif operation == 8:

        myDict.remove('a')

        return 'a' in myDict

    elif operation == 9:

        return b'\xab' in myDict

    return False
