
class MoreAwesome():
    """
    A little more complicated object
    """

    # it has some attributes
    thename = 'CoZ'
    intval = 32
    awesome = 42


    def mmmm(self, arg):

        res = self.add_thirteen_to_this(arg)

        return res


    def add_thirteen_to_this(self, arg):
        """
        Demonstrate accepting an argument besides just ``self``
        Args:
            arg: any type

        Returns:
            return the value of the argument plus the value of ``self`` intval property
        """
        print("adding thirdteen!")
        m = arg + 13

        return m
