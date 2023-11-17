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


# Exercise 4

:::{important}
Please complete this exercise
**by the end of day** on Thursday, 30 November, 2023
(the day of next week’s work session).
:::

To start this assignment, [accept the GitHub Classroom
assignment](https://classroom.github.com/a/h_RCOR5r), and clone *your own*
repository, e.g., in a [CSC
Notebook](../../course-info/course-environment)
instance. Make sure you commit and push all changes you make (you can
revisit instructions on how to use `git` and the jupyterlab git-plugin
on the [website of the Geo-Python
course](https://geo-python-site.readthedocs.io/en/latest/lessons/l2/git-basics.html).

To preview the exercise without logging in, you can find the open course copy
of the course’s GitHub repository at
[github.com/automating-gis-processes-2022/exercise-4](https://github.com/Automating-GIS-processes-II-2023/Exercise-4).
Don’t attempt to commit changes to that repository, but rather work with your
personal GitHub Classroom copy (see above).


## Hints

### Joining two data frames on different column names

We have already joined data sets that share the same index, and also used
*spatial joins* to merge geo-data frames depending on their geometric
relationships.

For *problem 1*, it might be handy to be able to join two data sets using
the values of two columns that have a different name. One good approach is to
set the index of both data frames to refer to the same column:

```{code-cell}
import pandas

df1 = pandas.DataFrame({
    "id": [1, 2, 3],
    "other_column": ["a", "b", "c"]
})

df1
```

```{code-cell}
df2 = pandas.DataFrame({
    "id": [67, 68, 69],
    "other_other_column": ["x", "y", "z"],
    "df1_id": [1, 2, 3]
})
df2
```

```{code-cell}
joint_df = df1.set_index("id").join(df2.set_index("df1_id"))
joint_df
```


### Renaming columns when joining data frames

It is often necessary to rename columns when we join data frames that have
duplicate column names. In the example below, both `df1` and `df2` have a
column `other_column`; the join fails. An appropriate fix is to add a suffix
to all columns of one or both of the data frames:

```{code-cell}
import pandas

df1 = pandas.DataFrame({
    "id": [1, 2, 3],
    "other_column": ["a", "b", "c"]
})

df1
```

```{code-cell}
df2 = pandas.DataFrame({
    "id": [67, 68, 69],
    "other_other_column": ["x", "y", "z"],
    "df1_id": [1, 2, 3]
})
df2
```

```{code-cell}
:tags: ["raises-exception"]
# Will fail, because duplicate column names exist:
joint_df = df1.join(df2)
joint_df
```

```{code-cell}
# works: add a suffix to one of the data sets’ columns
joint_df = df1.join(df2.add_suffix("_df2"))
joint_df
```


### Searching for files using a pattern

In [Lesson
2](../lesson-2/geopandas-an-introduction)
we discussed how to use a file pattern to search for files, using
[`pathlib.Path.glob()`](https://docs.python.org/3/library/pathlib.html#pathlib.Path.glob).

To loop over all files ending in `_s.shp` inside `DATA_DIRECTORY /
"finland_topographic_database`, use the following piece of code:

```{code-cell}
import pathlib
DATA_DIRECTORY = pathlib.Path().resolve() / "data"

for input_file in (DATA_DIRECTORY / "finland_topographic_database").glob("*_s.shp"):
    print(input_file.name)
```

This will come in handy for *problem 2*, when reading in all travel time data
files. Be sure to revisit the explanation in [Lesson
2](../lesson-2/geopandas-an-introduction).


### Find the minimum value across multiple columns

For *problem 2*, you have to find the smallest value across multiple columns:
the shortest travel time to any of the eight shopping centres. For this,
[`panda`’s `DataFrame.min()`
method](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.min.html)
can come in handy. It identifies the smallest value in each column or row (it
accepts the same `axis=` parameter as `apply()`).

For instance, to find the smalles value for each row across the columns `a`,
`b`, and `c` of the data frame below, use the following code:

```{code-cell}
import pandas

df = pandas.DataFrame(
    {
        "id": [1, 2, 3],
        "a": [27, 64, 12],
        "b": [13, 13, 13],
        "c": [34, 15, 1]
    }
)

df
```

```{code-cell}
# select which columns to compare, then call `.min()`
df[["a", "b", "c"]].min(axis=1)
```

To find out which column had the smallest value for each row, use the
near-identical method
[`idxmin()`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.idxmin.html):

```{code-cell}
df[["a", "b", "c"]].idxmin(axis=1)
```

Of course, equivalent methods to find the greatest values exist: they are named
[`pandas.DataFrame.max()`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.max.html)
and
[`pandas.DataFrame.idxmax()`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.idxmax.html).
