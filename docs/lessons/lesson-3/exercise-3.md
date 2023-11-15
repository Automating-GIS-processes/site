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


# Exercise 3

:::{important}
Please complete this exercise
**by the end of day** on Thursday, 23 November, 2023
(the day before next week’s work session).
:::

To start this assignment, [accept the GitHub classroom
assignment](https://classroom.github.com/a/4Mc7iYSB), and clone *your own*
repository, e.g., in a [CSC
Notebook](../../course-info/course-environment)
instance. Make sure you commit and push all changes you make (you can
revisit instructions on how to use `git` and the JupyterLab git-plugin
on the [website of the Geo-Python
course](https://geo-python-site.readthedocs.io/en/latest/lessons/L2/git-basics.html).

To preview the exercise without logging in, you can find the open course copy
of the course’s GitHub repository at
[github.com/Automating-GIS-processes-2022/Exercise-3](https://github.com/Automating-GIS-processes-II-2023/Exercise-3).
Don’t attempt to commit changes to that repository, but rather work with your
personal GitHub classroom copy (see above).


## Hints

### Coordinate reference systems
 
:::{caution}

Remember the difference between defining a CRS, and re-projecting a layer into
a new CRS!  Before re-projecting, the layer should have a valid CRS definition
which you can check like this: `data.crs`.
:::
 
To **define a projection**, assign a new CRS to a geo-data frame’s `crs`
property:

```{code}
data.crs = pyproj.CRS("EPSG:4326")
```

This will update the metadata, only. The actual coordinate values will remained
unmodified. Use this only if the original CRS definition is missing or invalid.

To **re-project** a `geopandas.GeoDataFrame`, use its `to_crs()` method:

```{code}
data = data.to_crs("EPSG:4326")
```

This will actually transform the geometry features of the data frame, *AND* re-define the CRS definition stored in the `.crs` property.
