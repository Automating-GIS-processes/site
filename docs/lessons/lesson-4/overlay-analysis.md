---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.14.1
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

# Geometric operations

## Overlay analysis

In this tutorial, the aim is to make an overlay analysis where we create a new layer based on geometries from a dataset that `intersect` with geometries of another layer. As our test case, we will select Polygon grid cells from `TravelTimes_to_5975375_RailwayStation_Helsinki.shp` that intersects with municipality borders of Helsinki found in `Helsinki_borders.shp`.

Typical overlay operations are (source: [QGIS docs](https://docs.qgis.org/2.8/en/docs/gentle_gis_introduction/vector_spatial_analysis_buffers.html#more-spatial-analysis-tools)):
![](img/overlay_operations.png)

## Download data

For this lesson, you should [download a data package](https://github.com/AutoGIS/data/raw/master/L4_data.zip) that includes 3 files:

 - Helsinki_borders.shp
 - Travel_times_to_5975375_RailwayStation.shp
 - Amazon_river.shp
 
 
You can download the data following these steps: 

1. Navigate to the correct folder:
 
```
cd autogis/notebooks/L4/data

```

2. Download the zip-file from https://github.com/AutoGIS/data/raw/master/L4_data.zip using wget

```
wget https://github.com/AutoGIS/data/raw/master/L4_data.zip

```

3. Unzip the file

```
$ unzip L4_data.zip
```

You should now see the files in the `data` folder.Let's first read the data and see how they look like.

```{code-cell} ipython3
import geopandas as gpd
import matplotlib.pyplot as plt
import shapely.speedups
%matplotlib inline

# File paths
border_fp = "data/Helsinki_borders.shp"
grid_fp = "data/TravelTimes_to_5975375_RailwayStation.shp"

# Read files
grid = gpd.read_file(grid_fp)
hel = gpd.read_file(border_fp)
```

Let's do a quick overlay visualization of the two layers:

```{code-cell} ipython3
# Plot the layers
ax = grid.plot(facecolor='gray')
hel.plot(ax=ax, facecolor='None', edgecolor='blue')
```

Here the grey area is the Travel Time Matrix - a data set that contains  13231 grid squares (13231 rows of data) that covers the Helsinki region, and the blue area represents the municipality of Helsinki. Our goal is to conduct an overlay analysis and select the geometries from the grid polygon layer that intersect with the Helsinki municipality polygon.

When conducting overlay analysis, it is important to first check that the CRS of the layers match. The overlay visualization indicates that everything should be ok (the layers are plotted nicely on top of each other). However, let's still check if the crs match using Python:

```{code-cell} ipython3
# Check the crs of the municipality polygon
print(hel.crs)
```

```{code-cell} ipython3
# Ensure that the CRS matches, if not raise an AssertionError
assert hel.crs == grid.crs, "CRS differs between layers!"
```

Indeed, they do. We are now ready to conduct an overlay analysis between these layers. 

We will create a new layer based on grid polygons that `intersect` with our Helsinki layer. We can use a function called `overlay()` to conduct the overlay analysis that takes as an input 1) first GeoDataFrame, 2) second GeoDataFrame, and 3) parameter `how` that can be used to control how the overlay analysis is conducted (possible values are `'intersection'`, `'union'`, `'symmetric_difference'`, `'difference'`, and `'identity'`):

```{code-cell} ipython3
intersection = gpd.overlay(grid, hel, how='intersection')
```

Let's plot our data and see what we have:

```{code-cell} ipython3
intersection.plot(color="b")
```

As a result, we now have only those grid cells that intersect with the Helsinki borders. If you look closely, you can also observe that **the grid cells are clipped based on the boundary.**

- Whatabout the data attributes? Let's see what we have:

```{code-cell} ipython3
intersection.head()
```

As we can see, due to the overlay analysis, the dataset contains the attributes from both input layers.

Let's save our result grid as a GeoJSON file that is commonly used file format nowadays for storing spatial data.

```{code-cell} ipython3
# Output filepath
outfp = "data/TravelTimes_to_5975375_RailwayStation_Helsinki.geojson"

# Use GeoJSON driver
intersection.to_file(outfp, driver="GeoJSON")
```

There are many more examples for different types of overlay analysis in [Geopandas documentation](http://geopandas.org/set_operations.html) where you can go and learn more.

+++

## Aggregating data

Data aggregation refers to a process where we combine data into groups. When doing spatial data aggregation, we merge the geometries together into coarser units (based on some attribute), and can also calculate summary statistics for these combined geometries from the original, more detailed values. For example, suppose that we are interested in studying continents, but we only have country-level data like the country dataset. If we aggregate the data by continent, we would convert the country-level data into a continent-level dataset.

In this tutorial, we will aggregate our travel time data by car travel times (column `car_r_t`), i.e. the grid cells that have the same travel time to Railway Station will be merged together.

- For doing the aggregation we will use a function called `dissolve()` that takes as input the column that will be used for conducting the aggregation:

```{code-cell} ipython3
# Conduct the aggregation
dissolved = intersection.dissolve(by="car_r_t")

# What did we get
dissolved.head()
```

- Let's compare the number of cells in the layers before and after the aggregation:

```{code-cell} ipython3
print(f'Rows in original intersection GeoDataFrame: {len(intersection)}')
print(f'Rows in dissolved layer: {len(dissolved)}')
```

Indeed the number of rows in our data has decreased and the Polygons were merged together.

What actually happened here? Let's take a closer look. 

- Let's see what columns we have now in our GeoDataFrame:

```{code-cell} ipython3
dissolved.columns
```

As we can see, the column that we used for conducting the aggregation (`car_r_t`) can not be found from the columns list anymore. What happened to it?

- Let's take a look at the indices of our GeoDataFrame:

```{code-cell} ipython3
dissolved.index
```

Aha! Well now we understand where our column went. It is now used as index in our `dissolved` GeoDataFrame. 

- Now, we can for example select only such geometries from the layer that are for example exactly 15 minutes away from the Helsinki Railway Station:

```{code-cell} ipython3
# Select only geometries that are within 15 minutes away
dissolved.loc[15]
```

```{code-cell} ipython3
# See the data type
type(dissolved.loc[15])
```

```{code-cell} ipython3
# See the data
dissolved.loc[15].head()
```

As we can see, as a result, we have now a Pandas `Series` object containing basically one row from our original aggregated GeoDataFrame.

Let's also visualize those 15 minute grid cells.

- First, we need to convert the selected row back to a GeoDataFrame:

```{code-cell} ipython3
# Create a GeoDataFrame
selection = gpd.GeoDataFrame([dissolved.loc[15]], crs=dissolved.crs)
```

- Plot the selection on top of the entire grid:

```{code-cell} ipython3
# Plot all the grid cells, and the grid cells that are 15 minutes a way from the Railway Station
ax = dissolved.plot(facecolor='gray')
selection.plot(ax=ax, facecolor='red')
```

## Simplifying geometries

+++

Sometimes it might be useful to be able to simplify geometries. This could be something to consider for example when you have very detailed spatial features that cover the whole world. If you make a map that covers the whole world, it is unnecessary to have really detailed geometries because it is simply impossible to see those small details from your map. Furthermore, it takes a long time to actually render a large quantity of features into a map. Here, we will see how it is possible to simplify geometric features in Python.

As an example we will use data representing the Amazon river in South America, and simplify it's geometries.

- Let's first read the data and see how the river looks like:

```{code-cell} ipython3
import geopandas as gpd

# File path
fp = "data/Amazon_river.shp"
data = gpd.read_file(fp)

# Print crs
print(data.crs)

# Plot the river
data.plot()
```

The LineString that is presented here is quite detailed, so let's see how we can generalize them a bit. As we can see from the coordinate reference system, the data is projected in a metric system using [Mercator projection based on SIRGAS datum](http://spatialreference.org/ref/sr-org/7868/). 

- Generalization can be done easily by using a Shapely function called `.simplify()`. The `tolerance` parameter can be used to adjusts how much geometries should be generalized. **The tolerance value is tied to the coordinate system of the geometries**. Hence, the value we pass here is 20 000 **meters** (20 kilometers).


```{code-cell} ipython3
# Generalize geometry
data['geom_gen'] = data.simplify(tolerance=20000)

# Set geometry to be our new simlified geometry
data = data.set_geometry('geom_gen')

# Plot 
data.plot()
```

Nice! As a result, now we have simplified our LineString quite significantly as we can see from the map.
