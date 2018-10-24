Geometric operations
====================

Overlay analysis
----------------

The aim here is to make an overlay analysis where we select only specific polygon cells from the data
based on the borders of municipality of Helsinki.

Let's first read the data.

.. code:: python

    import geopandas as gpd
    import matplotlib.pyplot as plt
    import shapely.speedups

    # Let's enable speedups to make queries faster
    shapely.speedups.enable()

    # File paths
    border_fp = "/home/geo/data/Helsinki_borders.shp"
    grid_fp = "/home/geo/data/TravelTimes_to_5975375_RailwayStation.shp"

    # Read files
    grid = gpd.read_file(grid_fp)
    hel = gpd.read_file(border_fp)

.. ipython:: python
   :suppress:

    import gdal
    import geopandas as gpd
    import os
    import matplotlib.pyplot as plt
    import shapely.speedups
    shapely.speedups.enable()
    border_fp = os.path.join(os.path.abspath('data'), "Helsinki_borders.shp")
    grid_fp = os.path.join(os.path.abspath('data'), "TravelTimes_to_5975375_RailwayStation.shp")
    grid = gpd.read_file(grid_fp)
    hel = gpd.read_file(border_fp)

Let's check that the coordinate systems match.

.. ipython:: python

    hel.crs
    grid.crs

Indeed, they do. This is pre-srequisite to conduct spatial operations between the layers (as their coordinates need to match).

Let's see how our datasets look like. We will use the Helsinki municipality layer as our basemap and
plot the other layer on top of that.

.. ipython:: python


    basemap = hel.plot()
    grid.plot(ax=basemap, facecolor='gray' linewidth=0.02);

    # Use tight layout
    @savefig helsinki_grid_borders.png width=7in
    plt.tight_layout()

Let's do an overlay analysis and select polygons from grid that intersect with our Helsinki layer.

.. note::

   This can be a slow procedure with less powerful computer. There is a way to
   overcome this issue by doing the analysis **in batches** which is explained below, see the performance-tip_.

.. ipython:: python

    result = gpd.overlay(grid, hel, how='intersection')

Let's plot our data and see what we have.

.. ipython:: python

    result.plot(color="b")
    @savefig helsinki_grid_borders_intersect.png width=7in
    plt.tight_layout()

Cool! Now as a result we have only those grid cells included that intersect with the Helsinki borders
and the grid cells are clipped based on the boundary.

Whatabout the data attributes? Let's see what we have.

.. ipython:: python

    result.head()

Nice! Now we have attributes from both layers included.

Let's see the length of the GeoDataFrame.

.. ipython:: python

    len(result)

And the original data.

.. ipython:: python

    len(grid)

Let's save our result grid as a GeoJSON file that is another commonly used file
format nowadays for storing spatial data.

.. code:: python

    resultfp = "/home/geo/data/TravelTimes_to_5975375_RailwayStation_Helsinki.geojson"

    # Use GeoJSON driver
    result.to_file(resultfp, driver="GeoJSON")

.. ipython:: python
   :suppress:

    resultfp = os.path.join(os.path.abspath('data'), "TravelTimes_to_5975375_RailwayStation_Helsinki.geojson"
    result.to_file(resultfp, driver="GeoJSON")

There are many more examples for different types of overlay analysis in `Geopandas documentation  <http://geopandas.org/set_operations.html>`_ where you can go and learn more.

.. _performance-tip:

.. hint::

    Overlay analysis such as ours with around 13 000 polygons is quite CPU intensive task which can be quite slow to execute. Luckily, doing such analysis in *batches* improves the
    performance dramatically (spatial lookups are much quicker that way). The code snippet below shows how to do it with batch size of 10 rows which takes only around 1.5 minutes to run the analysis in our computer instance.

    .. code:: python

        import geopandas as gpd
        import numpy as np

        # File paths
        border_fp = "/home/geo/data/Helsinki_borders.shp"
        grid_fp = "/home/geo/data/TravelTimes_to_5975375_RailwayStation.shp"

        # Read files
        grid = gpd.read_file(grid_fp)
        hel = gpd.read_file(border_fp)

        # Batch size
        b = 10

        # Number of iterations (round up with np.ceil) and convert to integer
        row_cnt = len(grid)
        iterations = int(np.ceil(row_cnt / b))

        # Final result
        final = gpd.GeoDataFrame()

        # Set the start and end index according the batch size
        start_idx = 0
        end_idx = start_idx + b

        for iteration in range(iterations):
            print("Iteration: %s/%s" % (iteration, iterations))

            # Make an overlay analysis using a subset of the rows
            result = gpd.overlay(grid[start_idx:end_idx], hel, how='intersection')

            # Append the overlay result to final GeoDataFrame
            final = final.append(result)

            # Update indices
            start_idx += b
            end_idx = start_idx + b

        # Save the output as GeoJSON
        outfp = "/home/geo/data/overlay_analysis_speedtest.geojson"
        final.to_file(outfp, driver="GeoJSON")

Aggregating data
----------------

Aggregating data can also be useful sometimes. What we mean by aggregation is that we basically merge Geometries into together by some common identifier.
Suppose we are interested in studying continents, but we only have country-level data like the country dataset.
By aggregation we would convert this into a continent-level dataset.

Let's aggregate our travel time data by car travel times, i.e. the grid cells that have the same travel time to Railway Station will be merged together.

.. ipython:: python

   result_aggregated = result.dissolve(by="car_r_t")
   result_aggregated.head()

Let's compare the number of cells in the layers before and after the aggregation.

.. ipython:: python

    len(result)
    len(result_aggregated)

Indeed the number of rows in our data has decreased and the Polygons were merged together.

Simplifying geometries
----------------------

Sometimes it might be useful to be able to simplify geometries. This could be something to consider for example
when you have very detailed spatial features that cover the whole world. If you make a map that covers the whole
world, it is unnecessary to have really detailed geometries because it is simply impossible to see those small details
from your map. Furthermore, it takes a long time to actually render a large quantity of features into a map. Here, we
will see how it is possible to simplify geometric features in Python by continuing the example from the previous tutorial
on data classification.

What we will do next is to only include the big lakes and simplify them slightly so that they are not as detailed.

- Let's start by reading the lakes data into Geopandas that we saved earlier.

.. ipython:: python
   :suppress:

      lakes_fp = os.path.join(os.path.abspath('data'), "lakes.shp")

.. code:: python

   lakes_fp = "/home/geo/lakes.shp"

.. ipython:: python

   lakes = gpd.read_file(lakes_fp)

- Include only big lakes

.. ipython:: python

    big_lakes = lakes.ix[lakes['small_big'] == 1].copy()

- Let's see how they look

.. ipython:: python


    big_lakes.plot(linewidth=0.05, color='blue');
    @savefig big_lakes.png width=7in
    plt.tight_layout()

The Polygons that are presented there are quite detailed, let's generalize them a bit.

- Generalization can be done easily by using a Shapely function called ``.simplify()``. The ``tolerance`` parameter is adjusts how much
geometries should be generalized. **The tolerance value is tied to the coordinate system of the geometries**.
Thus, here the value we pass is 300 **meters**.

.. ipython:: python

    big_lakes['geom_gen'] = big_lakes.simplify(tolerance=300)

- Let's set the geometry to be our new column, and plot the results.

.. ipython:: python

    big_lakes['geometry'] = big_lakes['geom_gen']
    big_lakes.plot(linewidth=0.05, color='blue')
    @savefig big_lakes_simplified.png width=7in
    plt.tight_layout()

Nice! As a result, now we have simplified our Polygons slightly (although the differences might be a bit hard to spot).