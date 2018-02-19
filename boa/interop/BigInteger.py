
class BigInteger(int):

    @staticmethod
    def FromBytes(data, signed=False):
        """
        Convert a bytearray into a BigInteger object

        :param data: a bytearray representing an integer
        :type data: bytearray

        :param signed: whether or not the bytearray is signed
        :type signed: bool

        :return: a BigInteger object
        :rtype: ``boa.blockchain.vm.BigInteger``

        """
        return BigInteger(int.from_bytes(data, 'little', signed=signed))

    def Equals(self, other):
        """
        Compare two BigInteger objects

        :param other: the BigInteger to compare this one with
        :type other: BigInteger

        :return: whether the two items are equal
        :rtype: bool

        """
        return super(BigInteger, self).__eq__(other)

    def ToByteArray(self, signed=True):
        """

        converts a big integer object into a bytearray

        :param signed: whether or not it should be signed
        :type signed: bool

        :return: a bytearray of representing the BigInteger
        :rtype: bytearray

        """

        if self < 0:
            try:
                return self.to_bytes(1 + ((self.bit_length() + 7) // 8), byteorder='little', signed=True)
            except Exception as e:
                print("coludnt convert negative number %s " % e)
                return False
        try:
            return self.to_bytes((self.bit_length() + 7) // 8, byteorder='little', signed=signed)
        except OverflowError:
            return self.to_bytes(1 + ((self.bit_length() + 7) // 8), byteorder='little', signed=signed)
        except Exception:
            print("COULD NOT CONVERT %s to byte array" % self)

    def __abs__(self, *args, **kwargs):  # real signature unknown
        return BigInteger(super(BigInteger, self).__abs__(*args, **kwargs))

    def __add__(self, *args, **kwargs):  # real signature unknown
        return BigInteger(super(BigInteger, self).__add__(*args, **kwargs))

    def __mod__(self, *args, **kwargs):  # real signature unknown
        return BigInteger(super(BigInteger, self).__mod__(*args, **kwargs))

    def __mul__(self, *args, **kwargs):  # real signature unknown
        return BigInteger(super(BigInteger, self).__mul__(*args, **kwargs))

    def __neg__(self, *args, **kwargs):  # real signature unknown
        return BigInteger(super(BigInteger, self).__neg__(*args, **kwargs))

    def __str__(self, *args, **kwargs):  # real signature unknown
        return super(BigInteger, self).__str__(*args, **kwargs)

    def __sub__(self, *args, **kwargs):  # real signature unknown
        return BigInteger(super(BigInteger, self).__sub__(*args, **kwargs))

    def __truediv__(self, *args, **kwargs):  # real signature unknown
        return BigInteger(int(super(BigInteger, self).__truediv__(*args, **kwargs)))


ZERO = BigInteger(0)
ONE = BigInteger(1)
