
class Awesome(object):
    """
    A very basic object
    """

    # it has some attributes
    myname = 'NEO'
    mycount = 25

    # and a method

    def awesome_name(self):
        """
        this demonstrates that the object can have te concept of ``self``

        Returns:
            return the value of the objects ``myname`` attribute
        """
        return self.myname


class MoreAwesome(object):
    """
    A little more complicated object
    """

    # it has some attributes
    thename = 'CoZ'
    intval = 32
    awesome = 42

    def mmmm(self, arg):

        print("hello1")
        return self.add_thirteen_to_this(arg)

    def add_thirteen_to_this(self, arg):
        """
        Demonstrate accepting an argument besides just ``self``
        Args:
            arg: any type

        Returns:
            return the value of the argument plus the value of ``self`` intval property
        """

        m = arg + self.intval

        return m

    def multiply_nums(self, a, b):
        """
        Demonstrates it can take more than 1 parameter
        Args:
            a: int: number to be multiplied
            b: int: number to be multiplied

        Returns:
            int: result of operation
        """
        return a * b

    def multiply_by_awesome(self, a):
        """
        Demonstrates accepting an argument and multiplying it by an attribute of ``self``
        Args:
            a: an int

        Returns:
            result of multiplication
        """
        return self.awesome * a

    def do_something_with_awesome(self, awe: Awesome):
        """
        Demonstrates that you can take another class instance as an argument
        and access a property of it
        Args:
            awe: (Awesome) an instance of the Awesome class

        Returns:
            the value of ``awe.mycount`` + 3
        """
        return awe.mycount + 3

    def make_awesome(self):
        """
        Demonstrates that you can instantiate a class inside another class
        Returns:
            the value of the new Awesome instance's ``mycount`` attribute minus 30
        """
        awe = Awesome()

        return awe.mycount - 30

    def instantiate_awesome(self, count_to_use) -> Awesome:

        awe = Awesome()
        awe.mycount = count_to_use

        return awe

    def accept_two_awesomes(self, awe1: Awesome, awe2: Awesome):

        total = awe1.mycount
        total += awe2.mycount
        return total
