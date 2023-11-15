---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.14.1
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
---

# Spatial join

*Spatial joins* are operations that combine data from two or more spatial data
sets based on their geometric relationship. In the previous sections, we got to
know two specific cases of spatial joins: [Point-in-polygon
queries](point-in-polygon-queries) and [intersects-queries](intersect). However,
there is more to using the geometric relationship between features and between
entire layers.

Spatial join operations require two input parameters: the *predicament*, i.e., the
geometric condition that needs to be met between two geometries, and the
*join-type*: whether only rows with matching geometries are kept, or all of one
input table’s rows, or all records. 

*Geopandas* (using `shapely` to implement geometric relationships) [supports a
standard set of geometric
predicates](https://geopandas.org/en/stable/docs/user_guide/mergingdata.html#binary-predicate-joins),
that is similar to most GIS analysis tools and applications:

- intersects
- contains
- within
- touches
- crosses
- overlaps

Geometric predicaments are expressed as verbs, so they have an intuitive
meaning. See the [shapely user
manual](https://shapely.readthedocs.io/en/stable/manual.html#binary-predicates)
for a detailed description of each geometric predicate.


:::{admonition} Binary geometric predicates
:class: hint

Shapely supports more *binary geometric predicates* than geopandas implements
for spatial joins. What are they? Can they be expressed by combining the
implemented ones?
:::


In terms of the *join-type*, geopandas implements three different options:

- *left*: keep all records of the *left* data frame, fill with empty values if
  no match, keep *left* geometry column
- *right*: keep all records of the *left* data frame, fill with empty values if
  no match, keep *right* geometry column
- *inner*: keep only records of matching records, keep *left* geometry column


:::{tip}
The [PyGIS
book](https://pygis.io/docs/e_spatial_joins.html) has a great overview of
spatial predicaments and join-types with explanatory drawings.
:::


---


## Load input data

As a practical example, let’s find the population density at each of the
addresses from [earlier in this lesson](geocoding-in-geopandas), by combining
the data set with data from a population grid.

The population grid data is available from [HSY, the Helsinki Region
Environmental
Services](https://www.hsy.fi/en/environmental-information/open-data/), for
instance via their WFS endpoint.

```{code-cell}
import pathlib 
NOTEBOOK_PATH = pathlib.Path().resolve()
DATA_DIRECTORY = NOTEBOOK_PATH / "data"
```


```{code}
import geopandas

addresses = geopandas.read_file(DATA_DIRECTORY / "addresses.gpkg")

population_grid = geopandas.read_file(
    (
        "https://kartta.hsy.fi/geoserver/wfs"
        "?service=wfs"
        "&version=2.0.0"
        "&request=GetFeature"
        "&typeName=asuminen_ja_maankaytto:Vaestotietoruudukko_2020"
        "&srsName=EPSG:3879"
    ),
)
population_grid.crs = "EPSG:3879"  # for WFS data, the CRS needs to be specified manually
```

```{code-cell}
:tags: ["remove-input", "remove-output"]

import geopandas

addresses = geopandas.read_file(DATA_DIRECTORY / "addresses.gpkg")

population_grid = geopandas.read_file(
    "https://avoidatastr.blob.core.windows.net/avoindata/AvoinData/"
    "6_Asuminen/Vaestotietoruudukko/Shp/Vaestotietoruudukko_2021_shp.zip"
)
population_grid = (
    population_grid[["ASUKKAITA", "geometry"]]
    .rename(columns={"ASUKKAITA": "asukkaita"})
)
```

:::{admonition} Concatenating long strings
:class: note

In the WFS address above, we split a long string across multiple lines. Strings
between parentheses are automatically concatenated (joint together), even
without any operator (e.g., `+`).

For the sake of clarity, the example has an additional set of parentheses, but
already the parentheses of the method call would suffice.
:::


---


```{code-cell}
population_grid.head()
```

The population grid has many columns, and all of its column names are in
Finnish. Let’s drop (delete) all of the columns except the population total,
and rename the remaining to English:

```{code-cell}
population_grid = population_grid[["asukkaita", "geometry"]]
population_grid = population_grid.rename(columns={"asukkaita": "population"})
```

Finally, calculate the population density by dividing the number of inhabitants
of each grid cell by its area in km²:

```{code-cell}
population_grid["population_density"] = (
    population_grid["population"]
    / (population_grid.area / 1_000_000)
)
population_grid.head()
```

:::{admonition} Coding style: big numbers, operators in multi-line expressions
:class: tip

If you need to use very large numbers, such as, in the above example, the *1
million* to convert m² to km², you can use underscore characters (`_`) as
thousands separators. The Python interpreter will treat a sequence of numbers
interleaved with underscores as a regular numeric value.
[You can use the same syntax to group
numbers](https://peps.python.org/pep-0515/) by a different logic, for instance,
to group hexadecimal or binary values into groups of four.

In case an expression, such as, e.g., a mathematical formula, spreads across
multiple lines, it is considered good coding style to place an operator at the
beginning of a new line, rather than let it trail in the previous line. This is
considered more readable, as explained in the [PEP-8 styling
guidelines](https://peps.python.org/pep-0008/#should-a-line-break-before-or-after-a-binary-operator)
:::


---


## Join input layers


Now we are ready to perform the spatial join between the two layers.
Remember: the aim is to find the population density around each of the address
points. We want to attach population density information from the
`population_grid` polygon layer to the `addresses` point layer, depending on
whether the **point is within the polygon**. During this operation, we want to
**retain the geometries of the point layer**.

Before we can go ahead with the join operation, we have to make sure the two
layers are in the same cartographic reference system:

```{code-cell}
:tags: ["raises-exception"]

assert addresses.crs == population_grid.crs, "CRS are not identical"
```

They do not share the same CRS, let’s reproject one of them:

```{code-cell}
population_grid = population_grid.to_crs(addresses.crs)
```

Now we are ready to carry out the actual spatial join using the
[`geopandas.GeoDataFrame.sjoin()`](https://geopandas.org/en/stable/docs/reference/api/geopandas.GeoDataFrame.sjoin.html)
method. Remember, we want to use a *within* geometric predicate and retain the
point layer’s geometries (in the example below the *left* data frame).

```{code-cell}
addresses_with_population_data = addresses.sjoin(
    population_grid,
    how="left",
    predicate="within"
)
addresses_with_population_data.head()
```


That looks great! We now have an address data set with population density
information attached to it. 


---


As a final task, let’s look at how to plot data using a *graduated*
cartographic visualisation scheme. 

The `geopandas.GeoDataFrame.plot()` method can vary the map colours depending on a column’s values by passing its name as a named argument `column`. On top of that, the method accepts many arguments to influence the style of the map. Among them are `scheme` and `cmap` that define the [categorisation scheme](https://geopandas.org/en/stable/gallery/choropleths.html), and the [colour map](https://matplotlib.org/stable/tutorials/colors/colormaps.html) used. Many more arguments are passed through to `matplotlib`, such as `markersize` to set the size of point symbols, and `facecolor` to set the colour of polygon areas. To draw a legend, set `legend` to `True`, to set the size of the figure, pass a tuple (with values in inch) as `figsize`.

```{code-cell}
ax = addresses_with_population_data.plot(
    figsize=(10, 10),
    column="population_density",
    cmap="Reds",
    scheme="quantiles",
    markersize=15,
    legend=True
)
ax.set_title("Population density around address points")
```


---


We can apply the same arguments to plot a population density map using the
entire `population_grid` data set:

```{code-cell}
ax = population_grid.plot(
    figsize=(10, 10),
    column="population_density",
    cmap="Reds",
    scheme="quantiles",
    legend=True
)
ax.set_title("Population density in the Helsinki metropolitan area")

```


---


Finally, remember to save the output data frame to a file. We can append it to
the existing *GeoPackage* by specifying a new layer name:

```{code-cell}
addresses_with_population_data.to_file(
    DATA_DIRECTORY / "addresses.gpkg",
    layer="addresses_with_population_data"
)
