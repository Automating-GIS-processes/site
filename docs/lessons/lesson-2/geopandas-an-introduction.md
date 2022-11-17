---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.14.0
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
---

# Geopandas: an introduction

In this section, we will cover the basics of *geopandas*, a Python library to
interact with geospatial vector data.

[Geopandas](https://geopandas.org/) provides an easy-to-use interface to vector
data sets. It combines the capabilities of *pandas*, the data analysis package
we got to know in the [Geo-Python
course](https://geo-python-site.readthedocs.io/en/latest/lessons/L5/pandas-overview.html),
with the geometry handling functionality of
[shapely](../lesson-1/geometry-objects), the [geo-spatial file format support
of fiona](vector-data-io) and the [map projection libraries of
pyproj](map-projections).

The main data structures in geopandas are `GeoDataFrame`s and `GeoSeries`. They
extend the functionality of `pandas.DataFrame`s and `pandas.Series`. This means
that **we can use all our *pandas* skills also when we work with
*geopandas*!**. 

:::{tip}

If you feel like you need to refresh your memory about pandas, head back to
[lesson
5](https://geo-python-site.readthedocs.io/en/latest/lessons/L5/pandas-overview.html)
and [lesson
6](https://geo-python-site.readthedocs.io/en/latest/notebooks/L6/advanced-data-processing-with-pandas.html)
of Geo-Python.
:::

There is one key difference between pandas’s data frames and geopandas’
[`GeoDataFrame`s](https://geopandas.org/en/stable/docs/user_guide/data_structures.html#geodataframe):
a `GeoDataFrame` contains an additional column for geometries. By default, the
name of this column is `geometry`, and it is a
[`GeoSeries`](https://geopandas.org/en/stable/docs/user_guide/data_structures.html#geoseries)
that contains the geometries (points, lines, polygons, ...) as
`shapely.geometry` objects.

```{code-cell} ipython3
:tags: [remove-input]

import pathlib
import geopandas
import numpy
import pandas

DATA_DIRECTORY = pathlib.Path().resolve() / "data"

HIGHLIGHT_STYLE = "background: #f66161;"

# so the following block is a bit of bad magic to make the table output look
# nice (this cell is hidden, we are only interested in a short table listing
# in which the geometry column is highlighted).
#
# For this, we
#    1. convert the geopandas back into a ‘normal’ pandas.DataFrame with a shortened
#       WKT string in the geometry column
#    1b. while doing so, get rid of most of the columns (rename the remaining ones)
#    2. apply the style to all cells in the column "geometry", and to the axis-1-index "geometry"

# Why did I got via a ‘plain’ `pandas.DataFrame`?
# `pandas.set_option("display.max_colwidth", 40)` was ignored, so this seemed like the cleanest way

df = geopandas.read_file(DATA_DIRECTORY / "finland_topographic_database" / "m_L4132R_p.shp")

df["geom"] = df.geometry.to_wkt().apply(lambda wkt: wkt[:40] + " ...")

df = df[["RYHMA", "LUOKKA", "geom"]]
df = df.rename(columns={"RYHMA": "GROUP", "LUOKKA": "CLASS", "geom": "geometry"})

(
    df.head().style
        .applymap(lambda x: HIGHLIGHT_STYLE, subset=["geometry"])
        .apply_index(lambda x: numpy.where(x.isin(["geometry"]), HIGHLIGHT_STYLE, ""), axis=1)
)
```

---


## Input data: Finnish topographic database 

In this lesson, we will work with the [National Land Survey of Finland (NLS)/Maanmittauslaitos (MML) topographic database](https://www.maanmittauslaitos.fi/en/maps-and-spatial-data/expert-users/product-descriptions/topographic-database). 
- The data set is licensed under the NLS’ [open data licence](https://www.maanmittauslaitos.fi/en/opendata-licence-cc40) (CC BY 4.0).
- The structure of the data is described in a [separate Excel file](http://www.nic.funet.fi/index/geodata/mml/maastotietokanta/2022/maastotietokanta_kohdemalli_eng_2019.xlsx).
- Further information about file naming is available at [fairdata.fi](https://etsin.fairdata.fi/dataset/5023ecc7-914a-4494-9e32-d0a39d3b56ae) (this link relates to the 2018 issue of the topographic database, but is still valid).

For this lesson, we have acquired a subset of the topographic database as
shapefiles from the Helsinki Region in Finland via the [CSC’s Paituli download
portal](https://paituli.csc.fi). You can find the files in `data/finland_topographic_database/`.

:::{figure} ../../static/images/lesson-2/paituli-download_700x650px.png
:alt: Screenshot of the Paituli download page

The Paituli *spatial download service* offers data from a long list of national institutes and agencies.
:::


---


## Read and explore geo-spatial data sets

Before we attempt to load any files, let’s not forget to defining a constant
that points to our data directory:

```{code-cell} ipython3
import pathlib 
NOTEBOOK_PATH = pathlib.Path().resolve()
DATA_DIRECTORY = NOTEBOOK_PATH / "data"
```

In this lesson, we will focus on **terrain objects** (Feature group:
"Terrain/1" in the topographic database). The Terrain/1 feature group contains
several feature classes. 

**Our aim in this lesson is to save all the Terrain/1
feature classes into separate files**.

*Terrain/1 features in the Topographic Database:*

|  feature class | Name of feature                                            | Feature group |
|----------------|------------------------------------------------------------|---------------|
| 32421          | Motor traffic area                                         | Terrain/1     |
| 32200          | Cemetery                                                   | Terrain/1     |
| 34300          | Sand                                                       | Terrain/1     |
| 34100          | Rock - area                                                | Terrain/1     |
| 34700          | Rocky area                                                 | Terrain/1     |
| 32500          | Quarry                                                     | Terrain/1     |
| 32112          | Mineral resources extraction area, fine-grained material   | Terrain/1     |
| 32111          | Mineral resources extraction area, coarse-grained material | Terrain/1     |
| 32611          | Field                                                      | Terrain/1     |
| 32612          | Garden                                                     | Terrain/1     |
| 32800          | Meadow                                                     | Terrain/1     |
| 32900          | Park                                                       | Terrain/1     |
| 35300          | Paludified land                                            | Terrain/1     |
| 35412          | Bog, easy to traverse forested                             | Terrain/1     |
| 35411          | Open bog, easy to traverse treeless                        | Terrain/1     |
| 35421          | Open fen, difficult to traverse treeless                   | Terrain/1     |
| 33000          | Earth fill                                                 | Terrain/1     |
| 33100          | Sports and recreation area                                 | Terrain/1     |
| 36200          | Lake water                                                 | Terrain/1     |
| 36313          | Watercourse area                                           | Terrain/1     |


:::{admonition} Search for files using a pattern
:class: hint

(#search-for-files-using-a-pattern)=
A `pathlib.Path` (such as `DATA_DIRECTORY`) has a handy method to list all
files in a directory (or subdirectories) that match a pattern:
[`glob()`](https://docs.python.org/3/library/pathlib.html#pathlib.Path.glob).
To list all shapefiles in our topographic database directory, we can use the
following expression:

```{code}
(DATA_DIRECTORY / "finland_topographic_database").glob("*.shp")
```

In the search pattern, `?` represents any one single character, `*` multiple
(or none, or one) characters, and `**` multiple characters that can include
subdirectories.

Did you notice the parentheses in the code example above? They work just like
they would in a mathematical expression: first, the expression inside the
parentheses is evaluated, only then, the code outside.
:::


If you take a quick look at the data directory using a file browser, you will
notice that the topographic database consists of *many* smaller files. Their
names follow a strictly defined 
[convention](https://etsin.fairdata.fi/dataset/5023ecc7-914a-4494-9e32-d0a39d3b56ae),
according to this file naming convention, all files that we interested in
(*Terrain/1* and *polygons*) start with a letter `m` and end with a `p`.

We can use the `glob()` pattern search functionality to find those files:

```{code-cell} ipython3
TOPOGRAPHIC_DATABASE_DIRECTORY = DATA_DIRECTORY / "finland_topographic_database"

TOPOGRAPHIC_DATABASE_DIRECTORY
```

```{code-cell} ipython3
list(TOPOGRAPHIC_DATABASE_DIRECTORY.glob("m*p.shp"))
```

(Note that `glob()` returns an iterator, but, for now, we quickly convert
it to a list)

It seems our input data set has only one file that matches our search pattern.
We can save its filename into a new variable, choosing the first item of the
list (index 0):

```{code-cell} ipython3
input_filename = list(TOPOGRAPHIC_DATABASE_DIRECTORY.glob("m*p.shp"))[0] 
```

Now, it’s finally time to open the file and look at its contents:

```{code-cell} ipython3
import geopandas
data = geopandas.read_file(input_filename)
```

First, check the data type of the read data set:

```{code-cell} ipython3
type(data)
```

Everything went fine, and we have a `geopandas.GeoDataFrame`. 
Let’s also explore the data: (1) print the first few rows, and 
(2) list the columns.

```{code-cell} ipython3
data.head()
```

```{code-cell} ipython3
data.columns
```

Oh boy! This data set has many columns, and all of the column names are in
Finnish.

Let’s select a few useful ones and also translate their names to
English. We’ll keep ’RYHMA’ and ’LUOKKA’ (‘group’ and ‘class’, respectively),
and, of course, the `geometry` column.

```{code-cell} ipython3
data = data[["RYHMA", "LUOKKA", "geometry"]]
```

Renaming a column in (geo)pandas works by passing a dictionary to
`DataFrame.rename()`. In this dictionary, the keys are the old names, the values
the new ones:

```{code-cell} ipython3
data = data.rename(
    columns={
        "RYHMA": "GROUP",
        "LUOKKA": "CLASS"
    }
)
```

How does the data set look now?

```{code-cell} ipython3
data.head()
```

:::{admonition} Check your understanding:
:class: hint

Use your pandas skills on this geopandas data set to figure out the following
information:

- How many rows does the data set have?
- How many unique classes?
- ... and how many unique groups?
:::


---

### Explore the data set in a map:

As geographers, we love maps. But beyond that, it’s always a good idea to
explore a new data set also in a map. To create a simple map of a
`geopandas.GeoDataFrame`, simply use its `plot()` method. It works similar to
pandas (see [Lesson 7 of the Geo-Python 
course](https://geo-python.github.io/site/notebooks/L7/matplotlib.html), but
**draws a map based on the geometries of the data set** instead of a chart.

```{code-cell} ipython3
data.plot()
```

Voilá! It is indeed this easy to produce a map out of an geospatial data set.
Geopandas automatically positions your map in a way that it covers the whole
extent of your data.

:::{note}
If you live in the Helsinki region, you might recognise some of the shapes in
the map ;)
:::

### Geometries in geopandas

Geopandas takes advantage of shapely’s geometry objects. Geometries are stored
in a column called *geometry*.

Let’s print the first 5 rows of the column `geometry`:

```{code-cell} ipython3
data.geometry.head()
```

Lo and behold, the `geometry` column contains familiar-looking values:
*Well-Known Text* (WKT) strings. Don’t be fooled, they are, in fact,
`shapely.geometry` objects (you might remember from [last week’s
lesson](../lesson-1/geometry-objects)) that, when `print()`ed or type-cast into
a `str`, are represented as a WKT string).

Since the geometries in a `GeoDataFrame` are stored as shapely objects, we can
use **shapely methods** to handle geometries in geopandas.

Let’s take a closer look at (one of) the polygon geometries in the terrain data
set, and try to use some of the shapely functionality we are already familiar
with. For the sake of clarity, first, we’ll work with the geometry of the very
first record, only:

```{code-cell} ipython3
# The value of the column `geometry` in row 0:
data.at[0, "geometry"]
```

```{code-cell} ipython3
# Print information about the area 
print(f"Area: {round(data.at[0, 'geometry'].area)} m².")
```

:::{admonition} Area measurement unit
:class: note

Here, we know the coordinate reference system (CRS) of the input data set. The
CRS also defines the unit of measurement (in our case, metres). That’s why we
can print the computed area including an area measurement unit (square metres).
:::


Let’s do the same for multiple rows, and explore different options of how to.
First, use the reliable and tried `iterrows()` pattern we learned in [lesson 6
of the Geo-Python course](https://geo-python.github.io/site/notebooks/L6/pandas/advanced-data-processing-with-pandas.html#Iterating-rows-and-using-self-made-functions-in-Pandas).

```{code-cell} ipython3
# Iterate over the first 5 rows of the data set
for index, row in data[:5].iterrows():
    polygon_area = row["geometry"].area
    print(f"The polygon in row {index} has a surface area of {polygon_area:0.1f} m².")
```

As you see, all **pandas** functions, such as the `iterrows()` method, are
available in geopandas without the need to call pandas separately. Geopandas
builds on top of pandas, and it inherits most of its functionality.

Of course the `iterrows()` pattern is not the most convenient and efficient way
to calculate the area of many rows. Both `GeoSeries` (geometry columns) and
`GeoDataFrame`s have an `area` property:

```{code-cell} ipython3
# the `area` property of a `GeoDataFrame`
data.area
```

```{code-cell} ipython3
# the `area property of a `GeoSeries`
data["geometry"].area
```

It’s straight-forward to create a new column holding the area:

```{code-cell} ipython3
data["area"] = data.area
data
```

:::{admonition} Descriptive statistics
:class: hint

Do you remember how to calculate the *minimum*, *maximum*, *sum*, *mean*, and
*standard deviation* of a pandas column? ([Lesson 5 of
Geo-Python](https://geo-python-site.readthedocs.io/en/latest/notebooks/L5/exploring-data-using-pandas.html#descriptive-statistics))
What are these values for the area column of the data set?
:::



## Write a subset of data to a file

[In the previous section](./vector-data-io.md#writing-geospatial-data-to-a-file), we
learnt how to write an entire `GeoDataFrame` to a file. We can also write a
filtered subset of a data set to a new file, e.g., to help with processing
complex data sets.

First, isolate the lakes in the input data set (class number `36200`, see table
above):

```{code-cell} ipython3
lakes = data[data.CLASS == 36200]
```

Then, plot the data subset to visually check whether it looks correct:

```{code-cell} ipython3
lakes.plot()
```

And finally, write the filtered data to a Shapefile:

```{code-cell} ipython3
lakes.to_file(DATA_DIRECTORY / "finland_topographic_database" / "lakes.shp")
```

Check the [Vector Data I/O](vector-data-io) section to see which data formats
geopandas can write to.



## Grouping data

A particularly useful method of (geo)pandas’ data frames is their grouping
function: [`groupby()`](https://pandas.pydata.org/docs/user_guide/groupby.html)
can **split data into groups** based on some criteria, **apply** a function
individually to each of the groups, and **combine** results of such an
operation into a common data structure.

We have used this function earlier: in [Geo-Python, 
lesson 6](https://geo-python-site.readthedocs.io/en/latest/notebooks/L6/advanced-data-processing-with-pandas.html#aggregating-data-in-pandas-by-grouping).

We can use *grouping* here to split our input data set into subsets that relate
to each of the `CLASS`es of terrain cover, then save a separate file for each
class.

Let’s start this by, again, taking a look at how the data set actually looks
like:

```{code-cell} ipython3
data.head()
```

Remember: the `CLASS` column contains information about a polygon’s land use
type. Use the
[`pandas.Series.unique()`](https://pandas.pydata.org/docs/reference/api/pandas.Series.unique.html)
method to list all values that occur:

```{code-cell} ipython3
data["CLASS"].unique()
```

To group data, use the data frame’s `groupby()` method, supply a column name as
a parameter:

```{code-cell} ipython3
grouped_data = data.groupby("CLASS")
grouped_data
```

So, `grouped_data` is a `DataFrameGroupBy` object. Inside a `GroupBy` object,
its property `groups` is a dictionary that works as a lookup table: it records
which rows belong to which group. The keys of the dictionary are the unique
values of the grouping column:

```{code-cell}
grouped_data.groups
```

However, one can also simply iterate over the entire `GroupBy` object. Let’s
count how many rows of data each group has:

```{code-cell}
for key, group in grouped_data:
    print(f"Terrain class {key} has {len(group)} rows.")
```

There are, for instance, 56 lake polygons (class `36200`) in the input data set.

To obtain all rows that belong to one particular group, use the `get_group()`
method, which returns a brand-new `GeoDataFrame`:

```{code-cell}
lakes = grouped_data.get_group(36200)
type(lakes)
```

:::{caution}
The index in the new data frame stays the same as in the ungrouped input data
set. This can be helpful, for instance, when you want to join the grouped data
back to the original input data.
:::


## Write grouped data to separate files

Now we have all the necessary tools in hand to split the input data into
separate data sets for each terrain class, and write the individual subsets to
new, separate, files. In fact, the code looks almost too simple, doesn’t it?

```{code-cell}
# Iterate over the input data, grouped by CLASS
for key, group in data.groupby("CLASS"):
    # save the group to a new shapefile
    group.to_file(TOPOGRAPHIC_DATABASE_DIRECTORY / f"terrain_{key}.shp")
```

:::{admonition} File name
:class: attention

We used a `pathlib.Path` combined with an f-string to generate the new output
file’s path and name. Check this week’s section [Managing file
paths](managing-file-paths), and [Geo-Python lesson
2](https://geo-python-site.readthedocs.io/en/latest/notebooks/L2/Python-basic-elements.html#f-string-formatting)
to revisit how they work.
:::


## Extra: save summary statistics to CSV spreadsheet

Whenever the results of an operation on a `GeoDataFrame` do not include a
geometry, the output data frame will automatically become a ‘plain’
`pandas.DataFrame`, and can be saved to the standard table formats.

One interesting application of this is to save basic descriptive statistics of
a geospatial data set into a CSV table. For instance, we might want to know the
area each terrain class covers. 

Again, we start by grouping the input data by terrain classes, and then compute
the sum of each classes’ area. This can be condensed into one line of code:

```{code-cell}
area_information = data.groupby("CLASS").area.sum()
area_information
```

We can then save the resulting table into a CSV file using the standard pandas
approach we learned about in [Geo-Python
lesson 5](https://geo-python-site.readthedocs.io/en/latest/notebooks/L5/processing-data-with-pandas.html#writing-data-to-a-file).

```{code-cell}
area_information.to_csv(TOPOGRAPHIC_DATABASE_DIRECTORY / "area_by_terrain_class.csv")
```
