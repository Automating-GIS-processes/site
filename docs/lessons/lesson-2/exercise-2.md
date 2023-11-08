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
**by the end of day** on Thursday, 16 November, 2023
(the day before the next work session).
:::

To start this assignment, [accept the GitHub classroom
assignment](https://classroom.github.com/a/CqrsixHD), and clone *your own*
repository, e.g., in a [CSC
Notebook](../../course-info/course-environment)
instance. Make sure you commit and push all changes you make (you can
revisit instructions on how to use `git` and the JupyterLab git-plugin
on the [website of the Geo-Python
course](https://geo-python-site.readthedocs.io/en/latest/lessons/L2/git-basics.html).

To preview the exercise without logging in, you can find the open course copy
of the course’s GitHub repository at
[github.com/Automating-GIS-processes-II-2023/Exercise-2](https://github.com/Automating-GIS-processes-II-2023/Exercise-2).
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



### Creating a new `geopandas.GeoDataFrame`: alternative 1

Sometimes, it makes sense to start from scratch with an empty data set and
gradually add records. Of course, this is also possible with geopandas’ data
frames, that can then be saved as a new geopackage or shapefile.

First, create a completely empty `GeoDataFrame`:

```{code-cell}
import geopandas

new_geodataframe = geopandas.GeoDataFrame()
```

Then, create shapely geometry objects and insert them into the data frame. To
insert a geometry object into the `geometry` column, and a name into the `name`
column, in a newly added row, use:

```{code-cell}
import shapely.geometry
polygon = shapely.geometry.Polygon(
    [
        (24.9510, 60.1690),
        (24.9510, 60.1698),
        (24.9536, 60.1698),
        (24.9536, 60.1690)
    ]
)
name = "Senaatintori"

new_geodataframe.loc[
    len(new_geodataframe),  # in which row,
    ["name", "geometry"]    # in which columns to save values
] = [name, polygon]

new_geodataframe
```

Before saving the newly created dataset, don’t forget to define a cartographic
reference system for it. Otherwise, you will have trouble reusing the file in
other programs:

```{code-cell}
new_geodataframe.crs = "EPSG:4326"
```

:::{hint}
In the example above, we used the `len(new_geodataframe)` as a row index
(which, in a newly created data frame is equivalent to the row number).  Since
rows are counted from 0, the number of rows (length of data frame) is one
greater than the address of the last row. This expression, thus, always adds a
new row, independent of the actual length of the data frame.

Note, that, strictly speaking, the index is independent from the row number,
but in newly created data frames there are identical.
:::


### Creating a new `geopandas.GeoDataFrame`: alternative 2

Often, it is more convenient, and more elegant, to first create a dictionary
to collect data, that can then be converted into a data frame all at once.

For this, first define a `dict` with the column names as keys, and empty `list`s
as values:

```{code-cell}
data = {
    "name": [],
    "geometry": []
}
```

Then, fill the dict with data:

```{code-cell}
import shapely.geometry

data["name"].append("Senaatintori")
data["geometry"].append(
    shapely.geometry.Polygon(
        [
            (24.9510, 60.1690),
            (24.9510, 60.1698),
            (24.9536, 60.1698),
            (24.9536, 60.1690)
        ]
    )
)
```

Finally, use this dictionary as input for a new `GeoDataFrame`. Don’t forget to
specify a CRS:

```{code-cell}
new_geodataframe = geopandas.GeoDataFrame(data, crs="EPSG:4326")
new_geodataframe
```

---

:::{note}
These two approaches result in identical `GeoDataFrame`s. Sometimes, one
technique is more convenient than the other. You should always evaluate
different ways of solving a problem, and find the most appropriate and efficient
solution (there is **always** more than one possible solution).
:::
