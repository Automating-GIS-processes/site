Exercise 1
==========

.. admonition:: Start your assignment

    You can start working on your copy of Exercise 1 by `accepting the GitHub Classroom assignment <https://classroom.github.com/a/Fl7SxVTn>`__.

    **Exercise 1 is due by the start of lecture on 5.11**.

You can also take a look at the open course copy of `Exercise 1 in the course GitHub repository <https://github.com/AutoGIS-2018/Exercise-1>`__ (does not require logging in).
Note that you should not try to make changes to this copy of the exercise, but rather only to the copy available via GitHub Classroom.

Hints
-----

Assert statements
~~~~~~~~~~~~~~~~~

Assertions are a way to ``assert``, or ensure, that the values being used in your scripts are going to be
suitable for what the code does. It is common to use ``assert`` statements with ``functions`` as they are a
good way to ensure the correct functionality of a function and guide the user to use function as intended.

One good example how to use assertions inside a function is to ensure that the values passed into the function are
of correct type. It is also common to test value ranges with assert, such as test that values are positive.
Consider following example that combines these two checks:

.. code:: python

    # A function for summing positive values
    def sum_positive_values(value1, value2):
        """Sums positive values together."""

        # Check that the input values are of correct type (i.e. integers or floats)
        # We can check if the type of the input value can be found from a list of "correct" data types
        # --------------------------------------------------------------------------------------------

        # value1 -parameter
        assert type(value1) in [int, float], "Input value for 'value1' needs to be integer or floating point number! Found: %s" % type(value1)

        # value2 -parameter
        assert type(value2) in [int, float], "Input value for 'value2' needs to be integer or floating point number! Found: %s" % type(value2)

        # Check that the input values are positive
        # ----------------------------------------
        assert value1 > 0, "'value1' needs to be higher than 0! Found: %s" % value1
        assert value2 > 0, "'value2' needs to be higher than 0! Found: %s" % value2

        # If all the tests were passed, do the calculation and return the output
        return value1 + value2


This example demonstrates how it is possible to check and control that the input values are appropriate for the
function, and guide the user how to use the function correctly with informative error messages.

Iterating multiple lists simultaneously
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In Python a function called ``zip()`` makes it easy to iterate over multiple lists at the same time.
Consider following example:

.. ipython:: python

    # Create lists
    dog_list = ['Blackie', 'Musti', 'Svarte']
    age_list = [4.5, 2, 15]

    # Iterate over the lists using zip() to print an informative message
    for dog, age in zip(dog_list, age_list):
        print(dog, 'is', age, 'years old.')

This example demonstrates how it was possible to take two lists (could be even more lists) and access the values
from them using the same index number.

.. note::

    This approach assumes that the length of the lists are identical. If not, you will most probably get ``IndexError`` because the list index is out of range.