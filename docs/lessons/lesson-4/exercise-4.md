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
**by the end of day** on Friday, 2 December, 2022
(the day of next week’s work session).
:::

To start this assignment, [accept the GitHub classroom
assignment](https://classroom.github.com/a/CHANGE_LINK_HERE), and clone *your own*
repository, e.g., in a [CSC
Notebook](../../course-info/course-environment)
instance. Make sure you commit and push all changes you make (you can
revisit instructions on how to use `git` and the JupyterLab git-plugin
on the [website of the Geo-Python
course](https://geo-python-site.readthedocs.io/en/latest/lessons/L2/git-basics.html).

To preview the exercise without logging in, you can find the open course copy
of the course’s GitHub repository at
[github.com/Automating-GIS-processes-2022/Exercise-4](https://github.com/Automating-GIS-processes-2022/Exercise-4).
Don’t attempt to commit changes to that repository, but rather work with your
personal GitHub classroom copy (see above).


## Hints

### Searching for files using a pattern

In [Lesson
2](../lesson-2/geopandas-an-introduction.md#search-for-files-using-a-pattern)
we discussed how to use a file pattern to search for files, using
[`pathlib.Path.glob()`](https://docs.python.org/3/library/pathlib.html#pathlib.Path.glob).

To loop over all files ending in `_s.shp` inside `DATA_DIRECTORY /
"finland_topographic_database`, use the following piece of code:

```{code-cell}
import pathlib
DATA_DIRECTORY = pathlib.Path().resolve() / "data"

for input_file in (DATA_DIRECTORY / "finland_topographic_database").glob("*_s.shp"):
    print(input_file
```

This will come in handy for *problem 2*, when reading in all travel time data
files. Be sure to revisit the explanation in [Lesson
2](../lesson-2/geopandas-an-introduction.md#search-for-files-using-a-pattern).
