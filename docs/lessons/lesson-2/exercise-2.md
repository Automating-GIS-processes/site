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


# Exercise 2

:::{important}
Please complete this exercise
**by the **end of day** on Thursday, 17 November, 2022**
(the day before the next work session).
:::

To start this assignment, [accept the GitHub classroom
assignment](https://classroom.github.com/a/aSlecihw), and clone *your own*
repository, e.g., in a [CSC
Notebook](../../course-info/course-environment)
instance. Make sure you commit and push all changes you make (you can
revisit instructions on how to use `git` and the JupyterLab git-plugin
on the [website of the Geo-Python
course](https://geo-python-site.readthedocs.io/en/latest/lessons/L2/git-basics.html).

To preview the exercise without logging in, you can find the open course copy
of the course’s GitHub repository at
[github.com/Automating-GIS-processes-2022/Exercise-2](https://github.com/Automating-GIS-processes-2022/Exercise-2).
Don’t attempt to commit changes to that repository, but rather work with your
personal GitHub classroom copy (see above).


## Hints

### Converting a `pandas.DataFrame`  into a `geopandas.GeoDataFrame`

Sometimes, we work with data that are in a non-spatial format (such as Excel
or CSV spreadsheets) but contain information on the location of records, for
instance, in columns for longitude and latitude values. While geopandas’s
`read_file()` function can read some formats, often, the safest way is to use
pandas to read the data set and then convert it to a `GeoDataFrame`.

Let’s assume, we read the following table using `pandas.read_csv()` into a
variable `df`:

```{code-cell}
:tags: ["remove-input"]

# sample data
import pandas
df = pandas.DataFrame({
    "longitude": [24.9557, 24.8353, 24.9587],
    "latitude": [60.1555, 60.1878, 60.2029]
})
```

```{code-cell}
df
```

The `geopandas.GeoDataFrame()` constructor accepts a `pandas.DataFrame` as an
input, but it does not automatically fill the `geometry` column. However, the
library comes with a handy helper function `geopandas.points_from_xy()`. As we
all know, a spatial data set should always have a coordinate reference system
(CRS) defined; we can specify the CRS of the input data, here, too:

```{code-cell}

import geopandas

gdf = geopandas.GeoDataFrame(
    df,
    geometry=geopandas.points_from_xy(df.longitude, df.latitude),
    crs="EPSG:4326"
)

gdf
```

Now, we have a ‘proper‘ `GeoDataFrame` with which we can do all geospatial
operations we would want to do.
