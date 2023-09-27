---
kernelspec:
  name: python3
  display_name: python3
jupytext:
  text_representation:
    extension: .md
    format_name: myst
    format_version: '0.13'
    jupytext_version: 1.14.1
---


# Exercise 1

:::{important}
Please complete this exercise
**by 3 pm** on Thursday, 9 November, 2023
(the day before the next work session).
:::

To start this assignment, [accept the GitHub classroom
assignment](https://classroom.github.com/a/KtZvBd1E), and clone *your own*
repository, e.g., in a [CSC
Notebook](../../course-info/course-environment)
instance. Make sure you commit and push all changes you make (you can
revisit instructions on how to use `git` and the JupyterLab git-plugin
on the [website of the Geo-Python
course](https://geo-python-site.readthedocs.io/en/latest/lessons/L2/git-basics.html).

To preview the exercise without logging in, you can find the open course copy
of the course’s GitHub repository at
[github.com/Automating-GIS-processes-II-2023/Exercise-1](https://github.com/Automating-GIS-processes-II-2023/Exercise-1).
Don’t attempt to commit changes to that repository, but rather work with your
personal GitHub classroom copy (see above).

:::{admonition} Exercises are done individually
All the weekly exercises need to be done individually in this period. 
So **NO pair programming** for exercises in this period. 

:::


## Hints

- [Geo-Python, lesson 4: Functions](https://geo-python-site.readthedocs.io/en/latest/notebooks/L4/functions.html)
- [Geo-Python, lesson 6: Iterating dataframe rows](https://geo-python-site.readthedocs.io/en/latest/notebooks/L6/advanced-data-processing-with-pandas.html#iterating-over-rows)
- [Geo-Python, lesson 6: Using assertions](https://geo-python-site.readthedocs.io/en/latest/notebooks/L6/gcp-5-assertions.html)

- [`assert` statements](#assert-statements)
- [Alternatives to `pandas.DataFrame.iterrows()` (problem&nbsp;3)](#alternatives-to-iterrows)
- [Iterating over multiple lists simultaneously](#iterating-over-multiple-lists-simultaneously)


(#assert-statements)=
### `assert` statements

*Assertions* are a language feature in Python that allows the programmer to
[assert](https://en.wiktionary.org/wiki/assert), ensure, that a certain
condition is met. They are a good way to check that variables are in a suitable
range for further computation. For instance, if a function converts a
temperature, it can test that its input value is not below absolute zero. In a
way, `assert` statements work similar to an electrical fuse: if input current
is higher than expected, the fuse blows to protect the appliance that comes
after. If input values are outside an expected range, the `assert` statement
fails with an error, and stops the program to protect the following code from
being executed with wrong input.

`assert` statements are often used in functions to ensure the input values are
acceptable. Consider the following example:

```{code-cell}

def divide(dividend, divisor):
    """Return the division of dividend by divisor."""
    assert divisor != 0, "Cannot divide by zero."
    return (dividend / divisor)

```


(#alternatives-to-iterrows)=
### Alternatives to `pandas.DataFrame.iterrows()` (problem&nbsp;3)

It is entirely possible to solve *problem 3* using the `iterrows()` pattern you
learnt in [lesson 6 of
Geo-Python](https://geo-python-site.readthedocs.io/en/latest/notebooks/L6/advanced-data-processing-with-pandas.html#iterating-over-rows),
and your code would look something like this:

```{code-cell}
import pandas
import shapely.geometry

data = pandas.DataFrame({"x": [10, 20, 30], "y": [1, 3, 4]})

# Option 1: iterate over DataFrame’s rows:

for i, row in data.iterrows():
    point = shapely.geometry.Point(row["x"], row["y"])
    # ...

```

**However**, there are better, faster, more elegant solutions that also are shorter to write.
Pandas’ `DataFrame`s have a method `apply()` that runs a user-defined function on each row or on each column (depending on the `axis` parameter, if `axis=1`, `apply()` works on rows).

The outputs of running the function repeatly (in parallel, to be precise) are collected in a `pandas.GeoSeries` that is the return value of `apply()` and can be assigned to a new column or row (we’ll learn about that in the next lesson, for now let’s convert the data into a list).

Let’s look at an easy example to illustrate how that works: We create a simple function that takes a row and multiplies its `x` and `y` values:

```{code-cell}

def multiply(row):
    """Multiply a row’s x and y values."""
    return (row["x"] * row["y"])

product = data.apply(multiply, axis=1)
# note how the function is not called here (no parentheses!),
# but only passed as a reference

product = list(product)
product
```

#### Pandas’ `apply()` method

Exactly the same can be done with the more complex example of creating a point geometry:

```{code-cell}

# Option 2: Define a custom function, and apply this function to the data frame

def create_point(row):
    """Create a Point geometry from a row with x and y values."""
    point = shapely.geometry.Point(row["x"], row["y"])
    return point

point_series = data.apply(create_point, axis=1)

```

#### `Apply()`ing an anonymous *lambda function*

Finally, for simple functions that fit into one single line, we can pass the
function in so-called ‘lambda notation’.  Lambda functions follow the syntax
`lambda arguments: return-value`, i.e., the keyword `lambda` followed by one or
more, comma-separated, argument names (input variables), a colon (`:`), and the
return value statement (e.g., a calculation). A lambda function that accepts
two arguments and returns their sum, would look like this: `lambda a, b: (a + b)`.

Lambda functions can only be used where they are defined, but offer a handy
short-cut to not need separate functions for simple expressions. They are very
common in data science projects, but should not be over-used: as a
rule-of-thumb, don’t use lambda functions if their code does not fit on one
(short) line.


:::{admonition} Lambda functions
:class: info

Read more about lambda functions in the official [Python documentation](https://docs.python.org/3/tutorial/controlflow.html#lambda-expressions).

:::


For the geo-spatial problem we discussed above, we can use a lambda function to
create a point ‘on-the-fly’:

```{code-cell}

# Option 3: Apply a lambda function to the data frame

point_series = data.apply(
    lambda row: shapely.geometry.Point(row["x"], row["y"]),
    axis=1
)

```


(#iterating-over-multiple-lists-simultaneously)=
### Iterating over multiple lists simultaneously

The [built-in Python function `zip()`](https://docs.python.org/3/library/functions.html#zip)
makes it easy to work with multiple lists at the same time. It combines two or
more lists and iterates over them in parallel, returning one value of each list
at a time. Consider the following example:

```{code-cell}
dog_names = ["Blackie", "Musti", "Svarte"]
dog_ages = [4.5, 2, 15]

# Iterate over the names and ages lists in parallel:
for name, age in zip(dog_names, dog_ages):
    print(f"{name} is {age} years old")
```

:::{admonition} Variable names
:class: note

This example illustrates quite well, why variable names should be chosen wisely: lists, for instance, almost always represent multiple values, so their names should be in plural (E.g., `dog_names`). In a loop, having more than one variable can become confusing quickly; refrain from using short names such as `i` or `j` for anything but a simple counter: use descriptive names such as `name` or `age` in the above example.
:::


:::{caution}
When iterating over lists of different length, zip would shorten all lists to the length of the shortest. By default, this happens **without warning or error message**, so be careful!
:::
