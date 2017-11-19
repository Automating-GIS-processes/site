Data reclassification
=====================

Reclassifying data based on specific criteria is a common task when doing GIS analysis.
The purpose of this lesson is to see how we can reclassify values based on some criteria which can be whatever, such as:

.. code::

    1. if available space in a pub is less than the space in my wardrobe

    AND

    2. the temperature outside is warmer than my beer

    ------------------------------------------------------

    IF TRUE: ==> I go and drink my beer outside
    IF NOT TRUE: ==> I go and enjoy my beer inside at a table

Even though, the above would be an interesting study case, we will use slightly more traditional cases to learn classifications.
We will use Corine land cover layer from year 2012, and a Travel Time Matrix data from Helsinki to classify some features of them based on our own
self-made classifier, or using a ready made classifiers that are commonly used e.g. when doing visualizations.

The target in this part of the lesson is to:

1. classify the lakes into big and small lakes where

    - a big lake is a lake that is larger than the average size of all lakes in our study region
    - a small lake ^ vice versa

2. use travel times and distances to find out

   - good locations to buy an apartment with good public tranportation accessibility to city center
   - but from a bit further away from city center where the prices are lower (or at least we assume so).

3. use ready made classifiers from pysal -module to classify travel times into multiple classes.

Download data
-------------

Download (and then extract) the dataset zip-package used during this lesson `from this link <https://github.com/Automating-GIS-processes/Lesson-4-Classification-overlay/raw/master/data/data.zip>`_.

You should have following Shapefiles in the ``data`` folder:

.. code:: bash

   $ cd /home/geo/L4/data
   $ ls
   Corine2012_Uusimaa.cpg      Helsinki_borders.cpg                       TravelTimes_to_5975375_RailwayStation.dbf
   Corine2012_Uusimaa.dbf      Helsinki_borders.dbf                       TravelTimes_to_5975375_RailwayStation.prj
   Corine2012_Uusimaa.prj      Helsinki_borders.prj                       TravelTimes_to_5975375_RailwayStation.shp
   Corine2012_Uusimaa.shp      Helsinki_borders.shp                       TravelTimes_to_5975375_RailwayStation.shx
   Corine2012_Uusimaa.shp.xml  Helsinki_borders.shx
   Corine2012_Uusimaa.shx      TravelTimes_to_5975375_RailwayStation.cpg

Data preparation
----------------

Before doing any classification, we need to prepare our data a little bit.

Let's read the data in and select only English columns from it and plot our data so that we can see how it looks like on a map.

.. ipython:: python
    :suppress:

      import gdal
      import geopandas as gpd
      import matplotlib.pyplot as plt
      import os

      fp = os.path.join(os.path.abspath('data'), "Corine2012_Uusimaa.shp")
      data = gpd.read_file(fp)

.. code::

   import geopandas as gpd
   import matplotlib.pyplot as plt

   # File path
   fp = "/home/data/Corine2012_Uusimaa.shp"

   data = gpd.read_file(fp)

Let's see what we have.

.. ipython:: python

   data.head(2)

Let's select only English columns

.. ipython:: python

   # Select only English columns
   selected_cols = ['Level1', 'Level1Eng', 'Level2', 'Level2Eng', 'Level3', 'Level3Eng', 'Luokka3', 'geometry']

   # Select data
   data = data[selected_cols]

   # What are the columns now?
   data.columns

Let's plot the data and use column 'Level3' as our color.

.. ipython:: python

   data.plot(column='Level3', linewidth=0.05)

   # Use tight layout and remove empty whitespace around our map
   @savefig corine-level3.png width=7in
   plt.tight_layout()

Let's see what kind of values we have in 'Level3Eng' column.

.. ipython:: python

   list(data['Level3Eng'].unique())

Okey we have plenty of different kind of land covers in our data. Let's select only lakes from our data. Selecting specific rows from a DataFrame
based on some value(s) is easy to do in Pandas / Geopandas using a specific indexer called ``.ix[]``, read more from `here <http://pandas.pydata.org/pandas-docs/stable/indexing.html#different-choices-for-indexing>`_..

.. ipython:: python

   # Select lakes (i.e. 'waterbodies' in the data) and make a proper copy out of our data
   lakes = data.ix[data['Level3Eng'] == 'Water bodies'].copy()
   lakes.head(2)

Calculations in DataFrames
--------------------------

Okey now we have our lakes dataset ready. The aim was to classify those lakes into small and big lakes based on **the average size of all lakes** in our
study area. Thus, we need to calculate the average size of our lakes.

Let's check the coordinate system.

.. ipython:: python

   # Check coordinate system information
   data.crs

Okey we can see that the units are in meters and we have a `UTM projection.  <https://en.wikipedia.org/wiki/Universal_Transverse_Mercator_coordinate_system>`_

Let's calculate first the are of our lakes.

.. ipython:: python

   # Calculate the area of lakes
   lakes['area'] = lakes.area

   # What do we have?
   lakes['area'].head(2)

Notice that the values are now in square meters.. Let's change those into square kilometers so they are easier to read. Doing calculations in Pandas / Geopandas
are easy to do:

.. ipython:: python

   lakes['area_km2'] = lakes['area'] / 1000000

   # What is the mean size of our lakes?
   l_mean_size = lakes['area_km2'].mean()
   l_mean_size

Okey so the size of our lakes seem to be approximately 1.58 square kilometers.

.. note::

   It is also easy to calculate e.g. sum or difference between two or more layers (plus all other mathematical operations), e.g.:

   .. code:: python

      # Sum two columns
      data['sum_of_columns'] = data['col_1'] + data['col_2']

      # Calculate the difference of three columns
      data['difference'] = data['some_column'] - data['col_1'] + data['col_2']

Classifying data
----------------

Creating a custom classifier
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Let's create a function where we classify the geometries into two classes based on a given ``threshold`` -parameter.
If the area of a polygon is lower than the threshold value (average size of the lake), the output column will get a value 0,
if it is larger, it will get a value 1. This kind of classification is often called a `binary classification <https://en.wikipedia.org/wiki/Binary_classification>`_.


First we need to create a function for our classification task. This function takes a single row of the GeoDataFrame as input,
plus few other parameters that we can use.

.. code::

   def binaryClassifier(row, source_col, output_col, threshold):
       # If area of input geometry is lower that the threshold value
       if row[source_col] < threshold:
           # Update the output column with value 0
           row[output_col] = 0
       # If area of input geometry is higher than the threshold value update with value 1
       else:
           row[output_col] = 1
       # Return the updated row
       return row

.. ipython:: python
   :suppress:

      def binaryClassifier(row, source_col, output_col, threshold):
          # If area of input geometry is lower that the threshold value
          if row[source_col] < threshold:
              # Update the output column with value 0
              row[output_col] = 0
          # If area of input geometry is higher than the threshold value update with value 1
          else:
              row[output_col] = 1
          # Return the updated row
          return row

Let's create an empty column for our classification

.. ipython:: python

   lakes['small_big'] = None

We can use our custom function by using a Pandas / Geopandas function called ``.apply()``.
Thus, let's apply our function and do the classification.

.. ipython:: python

   lakes = lakes.apply(binaryClassifier, source_col='area_km2', output_col='small_big', threshold=l_mean_size, axis=1)

Let's plot these lakes and see how they look like.

.. ipython:: python

   lakes.plot(column='small_big', linewidth=0.05, cmap="seismic")

   @savefig small-big-lakes.png width=6in
   plt.tight_layout()

Okey so it looks like they are correctly classified, good. As a final step let's save the lakes as a file to disk.

.. code:: python

    In [20]: outfp_lakes = r"/home/geo/lakes.shp"
    In [21]: lakes.to_file(outfp_lakes)

.. ipython:: python
   :suppress:

    outfp_lakes = os.path.join(os.path.abspath('data'), "lakes.shp")
    lakes.to_file(outfp_lakes)

.. note::

   There is also a way of doing this without a function but with the previous example might be easier to understand how the function works.
   Doing more complicated set of criteria should definitely be done in a function as it is much more human readable.

   Let's give a value 0 for small lakes and value 1 for big lakes by using an alternative technique:

   .. code:: python

      lakes['small_big_alt'] = None
      lakes.loc[lakes['area_km2'] < l_mean_size, 'small_big_alt'] = 0
      lakes.loc[lakes['area_km2'] >= l_mean_size, 'small_big_alt'] = 1

Multicriteria data classification
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

It also possible to do classifiers with multiple criteria easily in Pandas/Geopandas by extending the example that we started earlier.
Now we will modify our binaryClassifier function a bit so that it classifies the data based on two columns.

Let's call it customClassifier2 as it takes into account two criteria:

.. code:: python

   def customClassifier2(row, src_col1, src_col2, threshold1, threshold2, output_col):
       # 1. If the value in src_col1 is LOWER than the threshold1 value
       # 2. AND the value in src_col2 is HIGHER than the threshold2 value, give value 1, otherwise give 0
       if row[src_col1] < threshold1 and row[src_col2] > threshold2:
           # Update the output column with value 0
           row[output_col] = 1
       # If area of input geometry is higher than the threshold value update with value 1
       else:
           row[output_col] = 0

       # Return the updated row
       return row

.. ipython:: python
  :suppress:

    def customClassifier2(row, src_col1, src_col2, threshold1, threshold2, output_col):
        if row[src_col1] < threshold1 and row[src_col2] > threshold2:
            row[output_col] = 1
        else:
            row[output_col] = 0
        return row

Okey, now we have our classifier ready, let's use it to our data.

First, we need to read our Travel Time data from Helsinki into memory from the GeoJSON file that `we prepared earlier <Lesson4-geometric-operations.html>`_ with overlay analysis.

.. code:: python

   fp = r"/home/geo/TravelTimes_to_5975375_RailwayStation_Helsinki.geojson"

   # Read the GeoJSON file similarly as Shapefile
   acc = gpd.read_file(fp)

   # Let's see what we have
   acc.head(2)

.. ipython:: python
   :suppress:

     import gdal
     import geopandas as gpd
     import os
     fp = os.path.join(os.path.abspath('data'), "TravelTimes_to_5975375_RailwayStation_Helsinki.geojson")
     acc = gpd.read_file(fp)
     acc.head(2)

Okey we have plenty of different variables (see `from here the description <http://blogs.helsinki.fi/accessibility/helsinki-region-travel-time-matrix-2015/>`_
for all attributes) but what we are
interested in are columns called ``pt_r_tt`` which is telling the time in minutes that it takes to reach city center
from different parts of the city, and ``walk_d`` that tells the network distance by roads to reach city center
from different parts of the city (almost equal to Euclidian distance).

**The NoData values are presented with value -1**. Thus we need to remove those first.

.. ipython:: python

   acc = acc.ix[acc['pt_r_tt'] >=0]

Let's plot it and see how our data looks like.

.. ipython:: python

   import matplotlib.pyplot as plt

   # Plot using 9 classes and classify the values using "Fisher Jenks" classification
   acc.plot(column="pt_r_tt", scheme="Fisher_Jenks", k=9, cmap="RdYlBu", linewidth=0);

   # Use tight layour
   @savefig pt_time.png width=7in
   plt.tight_layout()

Okey so from this figure we can see that the travel times are lower in the south where
the city center is located but there are some areas of "good" accessibility also in some other areas
(where the color is red).

Let's also make a plot about walking distances

.. ipython:: python

   acc.plot(column="walk_d", scheme="Fisher_Jenks", k=9, cmap="RdYlBu", linewidth=0);

   # Use tight layour
   @savefig walk_distances.png width=7in
   plt.tight_layout();

Okey, from here we can see that the walking distances (along road network) reminds
more or less Euclidian distances.

Let's finally do our classification based on two criteria
and find out grid cells where the **travel time is lower or equal to 20 minutes** but they are further away
**than 4 km (4000 meters) from city center**.

Let's create an empty column for our classification results called "Suitable_area".

.. ipython:: python

   acc["Suitable_area"] = None

Now we are ready to apply our custom classifier to our data with our own criteria.

.. ipython:: python

   acc = acc.apply(customClassifier2, src_col1='pt_r_tt', src_col2='walk_d', threshold1=20, threshold2=4000, output_col="Suitable_area", axis=1)

Let's see what we got.

.. ipython:: python

   acc.head()

Okey we have new values in ``Suitable_area`` .column.

How many Polygons are suitable for us? Let's find out by using a Pandas function called ``value_counts()`` that return the count of
different values in our column.

.. ipython:: python

   acc['Suitable_area'].value_counts()

Okey so there seems to be nine suitable locations for us where we can try to find an appartment to buy
Let's see where they are located.

.. ipython:: python

   # Plot
   acc.plot(column="Suitable_area", linewidth=0);

   # Use tight layour
   @savefig suitable_areas.png width=7in
   plt.tight_layout();

A-haa, okey so we can see that suitable places for us with our criteria seem to be located in the
eastern part from the city center. Actually, those locations are along the metro line which makes them
good locations in terms of travel time to city center since metro is really fast travel mode.

.. todo::

   **Task:**

   Try to change your classification criteria and see how your results change! What places would be
   suitable for you to buy an apartment in Helsinki region? You can also change the travel mode and see how
   they change the results.


Classification based on common classifiers
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

`Pysal <http://pysal.readthedocs.io/en/latest/>`_ -module is an extensive Python library including various functions and tools to
do spatial data analysis. It also includes all of the most common data classifiers that are used commonly e.g. when visualizing data.
Available map classifiers in pysal -module are (`see here for more details <http://pysal.readthedocs.io/en/latest/library/esda/mapclassify.html>`_):

 - Box_Plot
 - Equal_Interval
 - Fisher_Jenks
 - Fisher_Jenks_Sampled
 - HeadTail_Breaks
 - Jenks_Caspall
 - Jenks_Caspall_Forced
 - Jenks_Caspall_Sampled
 - Max_P_Classifier
 - Maximum_Breaks
 - Natural_Breaks
 - Quantiles
 - Percentiles
 - Std_Mean
 - User_Defined

Let's apply one of those classifiers into our data and classify the travel times by public transport into 9 classes.

.. ipython:: python

  import pysal as ps

  # Define the number of classes
  n_classes = 9

The classifier needs to be initialized first with ``make()`` function that takes the number of desired classes as input parameter.

.. ipython:: python

  # Create a Natural Breaks classifier
  classifier = ps.Natural_Breaks.make(k=n_classes)

Now we can apply that classifier into our data quite similarly as in our previous examples.

.. ipython:: python

  # Classify the data
  classifications = acc[['pt_r_tt']].apply(classifier)

  # Let's see what we have
  classifications.head()

Okey, so we have a DataFrame where our input column was classified into 9 different classes (numbers 1-9) based on `Natural Breaks classification <http://wiki-1-1930356585.us-east-1.elb.amazonaws.com/wiki/index.php/Jenks_Natural_Breaks_Classification>`_.

Now we want to join that reclassification into our original data but let's first rename the column so that we recognize it later on.

.. ipython:: python

  # Rename the column so that we know that it was classified with natural breaks
  classifications.columns = ['nb_pt_r_tt']

  # Join with our original data (here index is the key
  acc = acc.join(classifications)

  # Let's see how our data looks like
  acc.head()

Great, now we have those values in our accessibility GeoDataFrame. Let's visualize the results and see how they look.

.. ipython:: python

    # Plot
    acc.plot(column="nb_pt_r_tt", linewidth=0, legend=True);

    # Use tight layour
    @savefig natural_breaks_pt_accessibility.png width=7in
    plt.tight_layout()

And here we go, now we have a map where we have used one of the common classifiers to classify our data into 9 classes.