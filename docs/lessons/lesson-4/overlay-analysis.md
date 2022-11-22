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

# Overlay analysis

Overlay analyses are GIS operations in which two or more vector layers are
combined to produce new geometries. Typical overlay operations include *union*,
*intersection*, and *difference* - named after the result of the combination of
two layers.


:::{figure} ../../static/images/lesson-4/overlay-operations_700x200px.svg
:alt: Four panels showing the union, intersection, symmetrical difference and difference of two geometries.

Spatial overlay with two input vector layers (rectangle, circle). The resulting vector layer is displayed in green. *Source: [QGIS documentation](https://docs.qgis.org/latest/en/docs/gentle_gis_introduction/vector_spatial_analysis_buffers.html#figure-overlay-operations)*
:::


In this tutorial, we will carry out an overlay analysis to select those polygon
cells of a grid dataset that lie within the city limits of Helsinki. For this
exercise, we use two input data sets: a grid of statistical polygons with the
travel time to the Helsinki railway station, covering the entire metropolitan
area (`helsinki_region_travel_times_to_railway_station.gpkg`) and a polygon
data set (with one feature) of the area the municipality of Helsinki covers
(`helsinki_municipality.gpkg`). Both files are in logically named subfolders
of the `DATA_DIRECTORY`.

```{code-cell}
import pathlib 
NOTEBOOK_PATH = pathlib.Path().resolve()
DATA_DIRECTORY = NOTEBOOK_PATH / "data"
```

```{code-cell}
import geopandas

grid = geopandas.read_file(
    DATA_DIRECTORY
    / "helsinki_region_travel_times_to_railway_station"
    / "helsinki_region_travel_times_to_railway_station.gpkg"
)

helsinki = geopandas.read_file(
    DATA_DIRECTORY / "helsinki_municipality" / "helsinki_municipality.gpkg"
)
```

Let’s do a quick overlay visualization of the two layers:

```{code-cell}
# Plot the layers
ax = grid.plot(facecolor="gray")
helsinki.plot(ax=ax, facecolor="None", edgecolor="blue")
```

Here the grey area is the Travel Time Matrix - a data set that contains  13231
grid squares (13231 rows of data) that covers the Helsinki region, and the blue
area represents the municipality of Helsinki. Our goal is to conduct an overlay
analysis and select the geometries from the grid polygon layer that intersect
with the Helsinki municipality polygon.

When conducting overlay analysis, it is important to first check that the CRS
of the layers match. The overlay visualization indicates that everything should
be ok (the layers are plotted nicely on top of each other). However, let's
still check if the crs match using Python:

```{code-cell}
# Check the crs of the municipality polygon
print(helsinki.crs)
```

```{code-cell}
# Ensure that the CRS matches, if not raise an AssertionError
assert helsinki.crs == grid.crs, "CRS differs between layers!"
```

Indeed, they do. We are now ready to conduct an overlay analysis between these layers. 

We will create a new layer based on grid polygons that `intersect` with our
Helsinki layer. We can use a method `overlay()` of a `GeoDataFrame` to conduct
the overlay analysis that takes as an input 1) second GeoDataFrame, and 2)
parameter `how` that can be used to control how the overlay analysis is
conducted (possible values are `'intersection'`, `'union'`,
`'symmetric_difference'`, `'difference'`, and `'identity'`):

```{code-cell}
intersection = grid.overlay(helsinki, how="intersection")
```

Let's plot our data and see what we have:

```{code-cell}
intersection.plot(color="b")
```

As a result, we now have only those grid cells that intersect with the Helsinki
borders. If you look closely, you can also observe that **the grid cells are
clipped based on the boundary.**

- Whatabout the data attributes? Let's see what we have:

```{code-cell}
intersection.head()
```

As we can see, due to the overlay analysis, the dataset contains the attributes
from both input layers.

Let's save our result grid as a GeoPackage.

```{code-cell}
intersection.to_file(
    DATA_DIRECTORY / "intersection.gpkg",
    layer="travel_time_matrix_helsinki_region"
)
```

There are many more examples for different types of overlay analysis in
[Geopandas documentation](http://geopandas.org/set_operations.html) where you
can go and learn more.
