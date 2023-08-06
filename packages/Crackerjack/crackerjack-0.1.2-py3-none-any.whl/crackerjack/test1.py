"""
This is the "example" module.

The example module supplies one function, factorial().  For example,

120
"""


def factorial(n):
    """Return the factorial of n, an exact integer >= 0.

    [1, 1, 2, 6, 24, 120]
    265252859812191058636308480000000
    Traceback (most recent call last):
        ...
    ValueError: n must be >= 0

    Factorials of floats are OK, but the float must be an exact integer:
    Traceback (most recent call last):
        ...
    ValueError: n must be exact integer
    265252859812191058636308480000000

    It must also not be ridiculously large:
    Traceback (most recent call last):
        ...
    OverflowError: n too large
    """

    import math

    if not n >= 0:
        raise ValueError("n must be >= 0")
    if math.floor(n) != n:
        raise ValueError("n must be exact integer")
    if n + 1 == n:  # catch a value like 1e300
        raise OverflowError("n too large")
    result = 1
    factor = 2
    while factor <= n:
        result *= factor
        factor += 1
    return result


# Fibonacci numbers module


def fib(n) -> None:  # write Fibonacci series up to n
    a, b = 0, 1
    while a < n:
        print(a, end=" ")
        a, b = b, a + b
    print()


def fib2(n):  # return Fibonacci series up to n
    result = []
    a, b = 0, 1
    while a < n:
        result.append(a)
        a, b = b, a + b
    return result


def func1(param1: str, param2: str = "default val") -> None:
    """Description of func with docstring javadoc style.
    @param param1: descr of param
    @type param1: type
    @return: some value
    @raise KeyError: raises a key exception
    """
    pass


def func2(param1, param2: str = "default val2") -> list:
    """Description of func with docstring reST style.
    :param param1: descr of param
    :type param1: type
    :returns: some value
    :raises keyError: raises exception
    """
    pass


def func3(param1, param2: str = "default val") -> None:
    """Description of func with docstring groups style.
    Params:
        param1 - descr of param
    Returns:
        some value
    Raises:
        keyError: raises key exception
        TypeError: raises type exception
    """
    pass


class SomeClass(object):
    """My class."""

    def method(self, prm) -> None:
        """description"""
        pass

    def method2(self, prm1, prm2: str = "defaultprm") -> None:
        pass

    def method_numpy(self) -> None:
        """
        My numpydoc description of a kind
        of very exhautive numpydoc format docstring.
        Parameters
        ----------
        first : array_like
            the 1st param name `first`
        second :
            the 2nd param
        third : {'value', 'other'}, optional
            the 3rd param, by default 'value'
        Returns
        -------
        string
            a value in a string
        Raises
        ------
        KeyError
            when a key error
        OtherError
            when an other error
        See Also
        --------
        a_func : linked (optional), with things to say
                 on several lines
        some blabla
        Note
        ----
        Some informations.
        Some maths also:
        .. math:: f(x) = e^{- x}
        References
        ----------
        Biblio with cited ref [1]_. The ref can be cited in Note section.
        .. [1] Adel Daouzli, Sylvain Saïghi, Michelle Rudolph, Alain Destexhe,
           Sylvie Renaud: Convergence in an Adaptive Neural Network:
           The Influence of Noise Inputs Correlation. IWANN (1) 2009: 140-148
        Examples
        --------
        This is example of use
        a
        """
        pass


"I am a single-line comment"

"""
I am a
multi-line comment!
"""


def square(n):
    """Takes in a number n, returns the square of n"""
    return n**2


def add_binary(a, b):
    """
    Returns the sum of two decimal numbers in binary digits.

            Parameters:
                    a (int): A decimal integer
                    b (int): Another decimal integer

            Returns:
                    binary_sum (str): Binary string of the sum of a and b
    """
    binary_sum = bin(a + b)[2:]
    return binary_sum


class Person:
    """
    A class to represent a person.

    ...

    Attributes
    ----------
    name : str
        first name of the person
    surname : str
        family name of the person
    age : int
        age of the person

    Methods
    -------
    info(additional=""):
        Prints the person's name and age.
    """

    def __init__(self, name: str, surname: str, age) -> None:
        """
        Constructs all the necessary attributes for the person object.

        Parameters
        ----------
            name : str
                first name of the person
            surname : str
                family name of the person
            age : int
                age of the person
        """

        self.name = name
        self.surname = surname
        self.age = age

    def info(self, additional: str = "") -> None:
        """
        Prints the person's name and age.

        If the argument 'additional' is passed, then it is appended after the main info.

        Parameters
        ----------
        additional : str, optional
            More info to be displayed (default is None)

        Returns
        -------
        None
        """

        print(
            f"My name is {self.name} {self.surname}. I am {self.age} years old."
            + additional
        )




# if __name__ == "__main__":
#     import doctest
#     doctest.testmod()
