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

# Point-in-polygon queries

Finding out if a certain point is located inside or outside of an area,
or finding out if a line intersects with another line or polygon are
fundamental geospatial operations that are often used e.g. to select
data based on location. Such spatial queries are one of the typical
first steps of the workflow when doing spatial analysis. Performing a
spatial join (will be introduced later) between two spatial datasets is
one of the most typical applications where Point in Polygon (PIP) query
is used.

For further reading about PIP and other geometric operations,
see Chapter 4.2 in Smith, Goodchild & Longley: [Geospatial Analysis - 6th edition](https://www.spatialanalysisonline.com/HTML/index.html).


## How to check if point is inside a polygon?

Computationally, detecting if a point is inside a polygon is most commonly done using a specific formula called [Ray Casting algorithm](https://en.wikipedia.org/wiki/Point_in_polygon#Ray_casting_algorithm).
Luckily, we do not need to create such a function ourselves for
conducting the Point in Polygon (PIP) query. Instead, we can take
advantage of [Shapely's binary predicates](https://shapely.readthedocs.io/en/stable/manual.html#binary-predicates)
that can evaluate the topolocical relationships between geographical
objects, such as the PIP as we're interested here.

## Point-in-polygon queries on `shapely` geometries

There are basically two ways of conducting PIP in Shapely:

1. using a function called
   [within()](https://shapely.readthedocs.io/en/stable/manual.html#object.within)
   that checks if a point is within a polygon
2. using a function called
   [contains()](https://shapely.readthedocs.io/en/stable/manual.html#object.contains)
   that checks if a polygon contains a point


:::{note}
Even though we are talking here about **Point** in Polygon
operation, it is also possible to check if a LineString or Polygon is
inside another Polygon.
:::


Let’s first create a couple of point geometries:

```{code-cell}
import shapely.geometry
point1 = shapely.geometry.Point(24.952242, 60.1696017)
point2 = shapely.geometry.Point(24.976567, 60.1612500)
```

... and a polygon:

```{code-cell}
polygon = shapely.geometry.Polygon(
    [
        (24.950899, 60.169158),
        (24.953492, 60.169158),
        (24.953510, 60.170104),
        (24.950958, 60.169990)
    ]
)
```

```{code-cell}
print(point1)
print(point2)
print(polygon)
```

Let’s check if the points are `within()` the polygon:

```{code-cell}
point1.within(polygon)
```

```{code-cell}
point2.within(polygon)
```

It seems that the first point is inside the polygon, but the second one is not.

We can turn the logic of the look-up around: Rather than check of the point is
within the polygon, we can also ask whether the polygon `contains()` the point:

```{code-cell}
polygon.contains(point1)
```

```{code-cell}
polygon.contains(point2)
```

:::{hint}
The two ways of checking the spatial relationship are complementary and yield
equivalent results;
[`contains()`](https://shapely.readthedocs.io/en/stable/manual.html#object.contains)
is inverse to
[`within()`](https://shapely.readthedocs.io/en/stable/manual.html#object.within),
and vice versa.

Then, which one should you use? Well, it depends:

-  if you have **many points and just one polygon** and you try to find out
   which one of them is inside the polygon: You might need to iterate over the
   points and check one at a time if it is **`within()`** the polygon.
-  if you have **many polygons and just one point** and you want to find out
   which polygon contains the point: You might need to iterate over the
   polygons until you find a polygon that **`contains()`** the point specified
:::


## Point-in-polygon queries on `geopandas.GeoDataFrame`s

In the following practical example we find which of the addresses we obtained
in the [geocoding section](geocoding-in-geopandas) are located within a certain
city district of Helsinki.

The data set we are using is from [Helsinki Region Infoshare](https://hri.fi/data/en_GB/dataset/helsingin-piirijako), and licensed under a [Creative-Commons-Attribution-4.0](https://creativecommons.org/licenses/by/4.0/) license.

```{code-cell}
import pathlib
NOTEBOOK_PATH = pathlib.Path().resolve()
DATA_DIRECTORY = NOTEBOOK_PATH / "data"
```

```{code-cell}
import geopandas

city_districts = geopandas.read_file(
    DATA_DIRECTORY / "helsinki_city_districts" / "helsinki_city_districts_2021.gpkg"
)
city_districts.head()
```

```{code-cell}
city_districts.plot()
```

Specifically, we want to find out which points are within the ‘Eteläinen’
(‘southern’) city district. Let’s start by obtaining a separate data set for
this district, loading the addresses data, and plotting a multi-layer map
that shows all districts, the ‘Eteläinen’ district, and all the points in
one map:

```{code-cell}
southern_district = city_districts[city_districts.name == "Eteläinen"]
southern_district
```

```{code-cell}
addresses = geopandas.read_file(DATA_DIRECTORY / "addresses.gpkg")
```

:::{admonition} Plotting multiple map layers
:class: hint

To plot several map layers in one figure, use the `ax` parameter to specify in
which *axes* data should be plotted. We used this in [lesson 7 of
Geo-Python](https://geo-python-site.readthedocs.io/en/latest/notebooks/L7/matplotlib.html) to add text to a plot, or modify axes’ properties.

The easiest way to obtain an *axes* is to save the first `plot()`’s
return value (see below). Another option is to create [`subplots()`](https://geo-python-site.readthedocs.io/en/latest/notebooks/L7/advanced-plotting.html#using-subplots), possibly with only one row and one column.
:::

```{code-cell}
axes = city_districts.plot(facecolor="grey")
southern_district.plot(ax=axes, facecolor="red")
addresses.plot(ax=axes, color="blue", markersize=5)
```

Some points are within the ‘Eteläinen’ district, but others are not. To find
out which are the ones inside the district, we can use a **point-in-polygon
query**, this time on the entire `geopandas.GeoDataFrame`. Its method
`within()` returns Boolean (`True`/`False`) values that indicate whether or not
a row’s geometry is contained in the supplied *other* geometry:


:::{admonition} geometry vs. geometry column
:class: caution

In the example below, we use `southern.at[0, "geometry"]` to obtain a single
value, a `shapely.geometry.Polygon`, instead of an entire column (a
`GeoSeries`). This is in order to match each row’s geometry of the entire
`addresses` data frame against *the same polygon*. If, in contrast, we would
run `within()` against a column, the operation would be carried out row-wise,
i.e. the first address point would be checked against the first polygon, the
second address point against the second polygon, and so forth.

Check the [documentation for
`within()`](https://geopandas.org/en/stable/docs/reference/api/geopandas.GeoSeries.within.html)
to learn more!
:::


```{code-cell}
addresses.within(southern_district.at[0, "geometry"])
```

This list of Boolean values, also called a *mask array* can be used to filter
the input data frame:

```{code-cell}
addresses_in_the_southern_district = addresses[
    addresses.within(southern_district.at[0, "geometry"])
]
addresses_in_the_southern_district
```

Finally, let’s plot this list of addresses one more time to visually verify
that all of them, indeed, are located within the ‘Eteläinen’ city district:

```{code-cell}
axes = city_districts.plot(facecolor="grey")
southern_district.plot(ax=axes, facecolor="red")

addresses_in_the_southern_district.plot(
    ax=axes,
    color="gold",
    markersize=5
)
```

Perfect! Now we are left with only the (golden) points which, indeed, are
inside the red polygon. That’s exactly what we wanted!
